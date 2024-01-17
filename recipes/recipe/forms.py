import pint
from django.core.exceptions import ValidationError
from django.forms import CharField
from django.utils.translation import gettext_lazy as _
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
