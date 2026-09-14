"""
NOVA/FORM — Custom Template Tags
"""

from django import template

register = template.Library()


@register.filter
def currency(value):
    """Format a decimal as currency."""
    try:
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return value


@register.filter
def multiply(value, arg):
    """Multiply value by arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value
