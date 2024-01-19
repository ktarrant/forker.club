from django import template

register = template.Library()


@register.filter
def servings(amount):
    """ Formats the amount to use fractional if less than 1, and only up to
    two decimal points if greater than 1 """
    if amount <= 0.0:
        return "{}".format(amount)
    elif amount < 1.0:
        return "1/{:.0f}".format(1.0 / amount)
    else:
        return "{:.2g}".format(amount)
