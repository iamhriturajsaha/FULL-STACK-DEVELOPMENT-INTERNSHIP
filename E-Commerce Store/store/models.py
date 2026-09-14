"""
NOVA/FORM — Database Models

Product catalog, orders, and order items with proper
relationships, indexes, and DecimalField for currency.
"""

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Product category."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"{reverse('store:shop')}?category={self.slug}"


class Product(models.Model):
    """Product in the NOVA/FORM catalog."""
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text='Original price before discount'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        related_name='products'
    )
    image = models.URLField(
        max_length=500, blank=True,
        help_text='Primary product image URL'
    )
    secondary_image = models.URLField(
        max_length=500, blank=True,
        help_text='Secondary product image URL (shown on hover)'
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    featured = models.BooleanField(default=False, db_index=True)
    new_arrival = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'created_at']),
            models.Index(fields=['featured', '-created_at']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    @property
    def is_on_sale(self):
        return self.compare_at_price and self.compare_at_price > self.price

    @property
    def discount_percentage(self):
        if self.is_on_sale:
            return int(((self.compare_at_price - self.price) / self.compare_at_price) * 100)
        return 0


class Order(models.Model):
    """Customer order."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders'
    )
    order_number = models.CharField(max_length=20, unique=True, db_index=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='United States')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Order {self.order_number}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_order_number():
        """Generate a unique order number like NF-2026-XXXXX."""
        from django.utils import timezone
        year = timezone.now().year
        uid = uuid.uuid4().hex[:5].upper()
        return f"NF-{year}-{uid}"


class OrderItem(models.Model):
    """Individual line item in an order. Stores snapshots of product data."""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"

    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)
