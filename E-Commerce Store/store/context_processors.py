"""
NOVA/FORM — Context Processors

Make cart data and site info available in all templates.
"""

from .services import CartService


def cart_context(request):
    """Add cart data to every template context."""
    cart = CartService(request)
    return {
        'cart_total_items': cart.get_total_items(),
        'cart_items': cart.get_items(),
        'cart_subtotal': cart.get_subtotal(),
        'cart_shipping': cart.get_shipping(),
        'cart_total': cart.get_total(),
        'cart_is_empty': cart.is_empty(),
    }


def site_context(request):
    """Add global site data to every template context."""
    return {
        'site_name': 'NOVA/FORM',
        'site_tagline': 'Contemporary objects for people who appreciate design.',
        'current_year': 2026,
    }
