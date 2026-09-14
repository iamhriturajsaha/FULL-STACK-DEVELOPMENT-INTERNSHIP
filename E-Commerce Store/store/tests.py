"""
NOVA/FORM — Test Suite

Comprehensive tests for models, views, authentication, cart, checkout,
orders, search, and security.
"""

from decimal import Decimal
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Product, Order, OrderItem
from .services import CartService


class CategoryModelTests(TestCase):
    def test_create_category(self):
        cat = Category.objects.create(name='Lighting', slug='lighting')
        self.assertEqual(str(cat), 'Lighting')
        self.assertEqual(cat.slug, 'lighting')

    def test_auto_slug(self):
        cat = Category.objects.create(name='My Category')
        self.assertEqual(cat.slug, 'my-category')


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Objects', slug='objects')
        self.product = Product.objects.create(
            name='Test Vase',
            slug='test-vase',
            description='A test vase.',
            short_description='Test vase.',
            price=Decimal('85.00'),
            category=self.category,
            stock_quantity=10,
            featured=True,
        )

    def test_str(self):
        self.assertEqual(str(self.product), 'Test Vase')

    def test_get_absolute_url(self):
        self.assertEqual(
            self.product.get_absolute_url(),
            reverse('store:product_detail', kwargs={'slug': 'test-vase'})
        )

    def test_is_in_stock(self):
        self.assertTrue(self.product.is_in_stock)
        self.product.stock_quantity = 0
        self.assertFalse(self.product.is_in_stock)

    def test_is_on_sale(self):
        self.assertFalse(self.product.is_on_sale)
        self.product.compare_at_price = Decimal('100.00')
        self.assertTrue(self.product.is_on_sale)
        self.assertEqual(self.product.discount_percentage, 15)

    def test_decimal_price(self):
        self.assertIsInstance(self.product.price, Decimal)

    def test_auto_slug(self):
        p = Product.objects.create(
            name='My New Product',
            description='Test',
            price=Decimal('50.00'),
            stock_quantity=5,
        )
        self.assertEqual(p.slug, 'my-new-product')


class OrderModelTests(TestCase):
    def test_order_number_generation(self):
        order = Order.objects.create(
            full_name='Test User',
            email='test@test.com',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            subtotal=Decimal('100.00'),
            shipping=Decimal('15.00'),
            total=Decimal('115.00'),
        )
        self.assertTrue(order.order_number.startswith('NF-'))
        self.assertEqual(str(order), f'Order {order.order_number}')


class HomeViewTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('store:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NOVA/FORM')


class ShopViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Lighting', slug='lighting')
        Product.objects.create(
            name='Test Lamp', slug='test-lamp', description='Test',
            price=Decimal('100.00'), category=self.category, stock_quantity=5,
        )

    def test_shop_page(self):
        response = self.client.get(reverse('store:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Lamp')

    def test_shop_category_filter(self):
        response = self.client.get(reverse('store:shop') + '?category=lighting')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Lamp')

    def test_shop_sort(self):
        response = self.client.get(reverse('store:shop') + '?sort=price_low')
        self.assertEqual(response.status_code, 200)

    def test_shop_invalid_category(self):
        response = self.client.get(reverse('store:shop') + '?category=nonexistent')
        self.assertEqual(response.status_code, 404)


class ProductDetailViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Objects', slug='objects')
        self.product = Product.objects.create(
            name='Test Vase', slug='test-vase', description='A vase.',
            price=Decimal('85.00'), category=self.category, stock_quantity=10,
        )

    def test_product_detail(self):
        response = self.client.get(
            reverse('store:product_detail', kwargs={'slug': 'test-vase'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Vase')
        self.assertContains(response, '85.00')

    def test_invalid_product(self):
        response = self.client.get(
            reverse('store:product_detail', kwargs={'slug': 'nonexistent'})
        )
        self.assertEqual(response.status_code, 404)


class AuthenticationTests(TestCase):
    def test_register(self):
        response = self.client.post(reverse('store:register'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

    def test_register_duplicate_email(self):
        User.objects.create_user('existing@test.com', 'existing@test.com', 'pass123')
        response = self.client.post(reverse('store:register'), {
            'first_name': 'Test',
            'email': 'existing@test.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')

    def test_login(self):
        User.objects.create_user('test@example.com', 'test@example.com', 'pass123')
        response = self.client.post(reverse('store:login'), {
            'username': 'test@example.com',
            'password': 'pass123',
        })
        self.assertEqual(response.status_code, 302)

    def test_login_invalid(self):
        response = self.client.post(reverse('store:login'), {
            'username': 'wrong@example.com',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        user = User.objects.create_user('test@example.com', 'test@example.com', 'pass123')
        self.client.login(username='test@example.com', password='pass123')
        response = self.client.get(reverse('store:logout'))
        self.assertEqual(response.status_code, 302)

    def test_account_requires_login(self):
        response = self.client.get(reverse('store:account'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)

    def test_checkout_requires_login(self):
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)


class CartTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Objects', slug='objects')
        self.product = Product.objects.create(
            name='Test Product', slug='test-product', description='Test',
            price=Decimal('50.00'), category=self.category, stock_quantity=5,
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse('store:cart_add'), {
            'product_id': self.product.id,
            'quantity': 1,
        })
        self.assertEqual(response.status_code, 302)  # Redirect to cart

    def test_add_to_cart_ajax(self):
        response = self.client.post(
            reverse('store:cart_add'),
            {'product_id': self.product.id, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_total_items'], 1)

    def test_add_exceeds_stock(self):
        response = self.client.post(
            reverse('store:cart_add'),
            {'product_id': self.product.id, 'quantity': 10},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('5', data['message'])

    def test_remove_from_cart(self):
        self.client.post(reverse('store:cart_add'), {
            'product_id': self.product.id, 'quantity': 1,
        })
        response = self.client.post(
            reverse('store:cart_remove'),
            {'product_id': self.product.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_total_items'], 0)

    def test_update_quantity(self):
        self.client.post(reverse('store:cart_add'), {
            'product_id': self.product.id, 'quantity': 1,
        })
        response = self.client.post(
            reverse('store:cart_update'),
            {'product_id': self.product.id, 'quantity': 3},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['cart_total_items'], 3)

    def test_cart_page(self):
        response = self.client.get(reverse('store:cart'))
        self.assertEqual(response.status_code, 200)

    def test_empty_cart(self):
        response = self.client.get(reverse('store:cart'))
        self.assertContains(response, 'empty')

    def test_add_invalid_product(self):
        response = self.client.post(
            reverse('store:cart_add'),
            {'product_id': 9999, 'quantity': 1},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        data = response.json()
        self.assertFalse(data['success'])


class CheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'test@example.com', 'test@example.com', 'pass123',
            first_name='Test', last_name='User',
        )
        self.category = Category.objects.create(name='Objects', slug='objects')
        self.product = Product.objects.create(
            name='Test Product', slug='test-product', description='Test',
            price=Decimal('100.00'), category=self.category, stock_quantity=5,
        )

    def test_checkout_empty_cart(self):
        self.client.login(username='test@example.com', password='pass123')
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 302)  # Redirect to shop

    def test_checkout_with_items(self):
        self.client.login(username='test@example.com', password='pass123')
        self.client.post(reverse('store:cart_add'), {
            'product_id': self.product.id, 'quantity': 2,
        })
        response = self.client.get(reverse('store:checkout'))
        self.assertEqual(response.status_code, 200)

    def test_place_order(self):
        self.client.login(username='test@example.com', password='pass123')
        self.client.post(reverse('store:cart_add'), {
            'product_id': self.product.id, 'quantity': 2,
        })
        response = self.client.post(reverse('store:checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'CA',
            'postal_code': '90210',
            'country': 'United States',
        })
        self.assertEqual(response.status_code, 302)

        # Verify order was created
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total, Decimal('200.00'))  # 2 × $100
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.user, self.user)

    def test_stock_decreases(self):
        self.client.login(username='test@example.com', password='pass123')
        self.client.post(reverse('store:cart_add'), {
            'product_id': self.product.id, 'quantity': 2,
        })
        self.client.post(reverse('store:checkout'), {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'address': '123 Test St',
            'city': 'Test City',
            'postal_code': '90210',
            'country': 'United States',
        })
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_quantity, 3)

    def test_cart_cleared_after_order(self):
        self.client.login(username='test@example.com', password='pass123')
        self.client.post(reverse('store:cart_add'), {
            'product_id': self.product.id, 'quantity': 1,
        })
        self.client.post(reverse('store:checkout'), {
            'full_name': 'Test',
            'email': 'test@example.com',
            'address': '123 Test St',
            'city': 'City',
            'postal_code': '12345',
            'country': 'US',
        })
        # Cart should be empty
        response = self.client.get(reverse('store:cart'))
        self.assertContains(response, 'empty')

    def test_server_side_price(self):
        """Verify prices are calculated server-side, not from client."""
        self.client.login(username='test@example.com', password='pass123')
        self.client.post(reverse('store:cart_add'), {
            'product_id': self.product.id, 'quantity': 1,
        })
        self.client.post(reverse('store:checkout'), {
            'full_name': 'Test',
            'email': 'test@example.com',
            'address': '123 Test St',
            'city': 'City',
            'postal_code': '12345',
            'country': 'US',
        })
        order = Order.objects.first()
        item = order.items.first()
        # Price should match DB, not any client-submitted value
        self.assertEqual(item.price, Decimal('100.00'))
        self.assertEqual(item.subtotal, Decimal('100.00'))


class SearchTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Lighting', slug='lighting')
        Product.objects.create(
            name='Arc Lamp', slug='arc-lamp', description='A beautiful lamp',
            price=Decimal('200.00'), category=self.category, stock_quantity=10,
        )

    def test_search_results(self):
        response = self.client.get(reverse('store:search') + '?q=lamp')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Arc Lamp')

    def test_search_no_results(self):
        response = self.client.get(reverse('store:search') + '?q=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No results')

    def test_empty_search(self):
        response = self.client.get(reverse('store:search'))
        self.assertEqual(response.status_code, 200)

    def test_search_by_category(self):
        response = self.client.get(reverse('store:search') + '?q=lighting')
        self.assertContains(response, 'Arc Lamp')


class OrderHistoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'test@example.com', 'test@example.com', 'pass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            address='123 Test St',
            city='Test City',
            postal_code='12345',
            subtotal=Decimal('100.00'),
            shipping=Decimal('15.00'),
            total=Decimal('115.00'),
        )

    def test_account_shows_orders(self):
        self.client.login(username='test@example.com', password='pass123')
        response = self.client.get(reverse('store:account'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.order.order_number)

    def test_order_detail(self):
        self.client.login(username='test@example.com', password='pass123')
        response = self.client.get(
            reverse('store:order_detail', kwargs={'order_number': self.order.order_number})
        )
        self.assertEqual(response.status_code, 200)

    def test_cannot_view_other_user_order(self):
        other_user = User.objects.create_user('other@test.com', 'other@test.com', 'pass123')
        self.client.login(username='other@test.com', password='pass123')
        response = self.client.get(
            reverse('store:order_detail', kwargs={'order_number': self.order.order_number})
        )
        self.assertEqual(response.status_code, 404)


class AboutViewTests(TestCase):
    def test_about_page(self):
        response = self.client.get(reverse('store:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'NOVA/FORM')
