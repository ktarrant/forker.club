import pint
import datetime
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.utils.translation import gettext_lazy as _, gettext
from django.contrib.contenttypes.models import ContentType
from django_comments.signals import comment_was_posted
from mezzanine.generic.forms import ThreadedCommentForm
from mezzanine.utils.cache import add_cache_bypass
from mezzanine.utils.deprecation import is_authenticated
from mezzanine.utils.email import split_addresses, send_mail_template
from mezzanine.utils.views import ip_for_request
from mezzanine.conf import settings

from recipe.measurements import supported_units


unit_reg = pint.UnitRegistry()


class UnitField(CharField):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return unit_reg.Unit("")
        return unit_reg.Unit(value)

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)

        try:
            unit = unit_reg.Unit(value)
        except pint.errors.UndefinedUnitError:
            raise ValidationError(
                _("Unknown unit: %(value)s"),
                params={"value": value},
            )

        # TODO: We can expand the supported units on a per-good basis
        if unit not in supported_units:
            raise ValidationError(
                _("Unsupported unit: %(value)s"),
                params={"value", value}
            )


class SlimCommentForm(ThreadedCommentForm):

    """
    A comment form which matches the default djanago.contrib.comments one, but with 3 removed fields
    """
    def get_comment_create_data(self, site_id=None):
        # Use the data of the superclass, and remove extra fields
        return dict(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = self.target_object._get_pk_val(),  # force_unicode ?
            comment      = self.cleaned_data["comment"],
            submit_date  = datetime.datetime.now(),
            site_id      = settings.SITE_ID,
            is_public    = True,
            is_removed   = False,
        )

    def save(self, request):
        """
        Saves a new comment and sends any notification emails.
        """
        comment = self.get_comment_object()
        obj = comment.content_object
        if is_authenticated(request.user):
            comment.user = request.user
            comment.user_name = request.user.username
        comment.by_author = request.user == getattr(obj, "user", None)
        comment.ip_address = ip_for_request(request)
        comment.replied_to_id = self.data.get("replied_to")

        # Mezzanine's duplicate check that also checks `replied_to_id`.
        lookup = {
            "content_type": comment.content_type,
            "object_pk": comment.object_pk,
            "user_name": comment.user_name,
            "user_email": comment.user_email,
            "user_url": comment.user_url,
            "replied_to_id": comment.replied_to_id,
        }
        for duplicate in self.get_comment_model().objects.filter(**lookup):
            if (
                duplicate.submit_date.date() == comment.submit_date.date()
                and duplicate.comment == comment.comment
            ):
                return duplicate

        comment.save()
        comment_was_posted.send(
            sender=comment.__class__, comment=comment, request=request
        )

        notify_emails = split_addresses(settings.COMMENTS_NOTIFICATION_EMAILS)
        if notify_emails:
            subject = gettext("New comment for: ") + str(obj)
            context = {
                "comment": comment,
                "comment_url": add_cache_bypass(comment.get_absolute_url()),
                "request": request,
                "obj": obj,
            }
            send_mail_template(
                subject,
                "email/comment_notification",
                settings.DEFAULT_FROM_EMAIL,
                notify_emails,
                context,
            )
        return comment


SlimCommentForm.base_fields.pop('url')
SlimCommentForm.base_fields.pop('email')
SlimCommentForm.base_fields.pop('name')