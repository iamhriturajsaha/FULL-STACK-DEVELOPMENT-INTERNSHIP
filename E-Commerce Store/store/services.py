"""
NOVA/FORM — Business Logic Services

Cart management (session-backed) and order processing with
server-side validation, atomic transactions, and stock management.
"""

from decimal import Decimal
from django.db import transaction
from django.db.models import F
from .models import Product, Order, OrderItem


class CartService:
    """
    Session-backed shopping cart.
    Cart structure in session: {'cart': {'product_id': quantity}}
    All prices are looked up server-side from the database.
    """

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart

    def _save(self):
        """Mark session as modified to persist changes."""
        self.session.modified = True

    def add(self, product_id, quantity=1):
        """
        Add a product to cart or increase its quantity.
        Returns (success, message) tuple.
        """
        product_id = str(product_id)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return False, 'Product not found.'

        current_qty = self.cart.get(product_id, 0)
        new_qty = current_qty + quantity

        if new_qty > product.stock_quantity:
            if product.stock_quantity == 0:
                return False, 'This product is out of stock.'
            return False, f'Only {product.stock_quantity} available.'

        self.cart[product_id] = new_qty
        self._save()
        return True, f'{product.name} added to bag.'

    def remove(self, product_id):
        """Remove a product from the cart entirely."""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self._save()
            return True, 'Removed from bag.'
        return False, 'Product not in bag.'

    def update_quantity(self, product_id, quantity):
        """Set exact quantity for a product."""
        product_id = str(product_id)
        if product_id not in self.cart:
            return False, 'Product not in bag.'

        if quantity <= 0:
            return self.remove(product_id)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return self.remove(product_id)

        if quantity > product.stock_quantity:
            return False, f'Only {product.stock_quantity} available.'

        self.cart[product_id] = quantity
        self._save()
        return True, 'Quantity updated.'

    def get_items(self):
        """
        Return list of cart items with full product data and line totals.
        Removes any products that no longer exist.
        """
        product_ids = list(self.cart.keys())
        products = Product.objects.filter(id__in=product_ids).select_related('category')

        items = []
        found_ids = set()
        for product in products:
            pid = str(product.id)
            found_ids.add(pid)
            quantity = self.cart[pid]
            items.append({
                'product': product,
                'quantity': quantity,
                'line_total': product.price * quantity,
            })

        # Clean up removed products
        removed = set(product_ids) - found_ids
        if removed:
            for pid in removed:
                del self.cart[pid]
            self._save()

        return items

    def get_subtotal(self):
        """Calculate cart subtotal from database prices."""
        items = self.get_items()
        return sum(item['line_total'] for item in items)

    def get_total_items(self):
        """Total number of items in cart."""
        return sum(self.cart.values())

    def get_shipping(self, subtotal=None):
        """Calculate shipping. Free over $150."""
        if subtotal is None:
            subtotal = self.get_subtotal()
        if subtotal >= Decimal('150.00'):
            return Decimal('0.00')
        return Decimal('15.00')

    def get_total(self):
        """Calculate order total."""
        subtotal = self.get_subtotal()
        shipping = self.get_shipping(subtotal)
        return subtotal + shipping

    def clear(self):
        """Empty the cart."""
        self.session['cart'] = {}
        self._save()

    def is_empty(self):
        """Check if cart has items."""
        return len(self.cart) == 0

    def __len__(self):
        return self.get_total_items()


class OrderService:
    """
    Order creation with atomic transactions,
    server-side price validation, and stock management.
    """

    @staticmethod
    @transaction.atomic
    def create_order(user, cart_service, checkout_data):
        """
        Create an order from the current cart.
        All prices are read from the database — never from the client.
        Uses transaction.atomic() to ensure data integrity.

        Returns (order, error_message) tuple.
        """
        items = cart_service.get_items()
        if not items:
            return None, 'Your bag is empty.'

        # Validate stock (inside transaction for consistency)
        for item in items:
            product = Product.objects.select_for_update().get(id=item['product'].id)
            if item['quantity'] > product.stock_quantity:
                return None, f'"{product.name}" only has {product.stock_quantity} in stock.'

        # Calculate totals server-side
        subtotal = sum(item['line_total'] for item in items)
        shipping = cart_service.get_shipping(subtotal)
        total = subtotal + shipping

        # Create order
        order = Order.objects.create(
            user=user if user.is_authenticated else None,
            full_name=checkout_data['full_name'],
            email=checkout_data['email'],
            address=checkout_data['address'],
            city=checkout_data['city'],
            state=checkout_data.get('state', ''),
            postal_code=checkout_data['postal_code'],
            country=checkout_data.get('country', 'United States'),
            subtotal=subtotal,
            shipping=shipping,
            total=total,
            status='pending',
        )

        # Create order items and decrement stock
        for item in items:
            product = item['product']
            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=item['quantity'],
                subtotal=item['line_total'],
            )
            # Decrement stock
            Product.objects.filter(id=product.id).update(
                stock_quantity=F('stock_quantity') - item['quantity']
            )

        # Clear cart
        cart_service.clear()

        return order, None
