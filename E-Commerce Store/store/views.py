"""
NOVA/FORM — Views

All page views and AJAX endpoints for the e-commerce site.
Business logic is delegated to services.py.
"""

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Product, Category, Order
from .services import CartService, OrderService
from .forms import RegistrationForm, LoginForm, CheckoutForm


# ─── PUBLIC PAGES ──────────────────────────────────────────────

def splash(request):
    """Introductory splash page."""
    return render(request, 'splash.html', {
        'page_title': 'NOVA/FORM',
    })

def home(request):
    """Homepage with hero, featured products, and editorial sections."""
    featured = Product.objects.filter(
        featured=True, stock_quantity__gt=0
    ).select_related('category')[:8]

    new_arrivals = Product.objects.filter(
        new_arrival=True, stock_quantity__gt=0
    ).select_related('category')[:6]

    categories = Category.objects.all()

    return render(request, 'home.html', {
        'featured_products': featured,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'page_title': 'NOVA/FORM — Contemporary Objects',
        'meta_description': 'NOVA/FORM — Contemporary objects for people who appreciate design. Curated collection of lighting, furniture, objects, and accessories.',
    })


def shop(request):
    """Product catalog with filtering and sorting."""
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    # Category filter
    category_slug = request.GET.get('category')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    # Sorting
    sort = request.GET.get('sort', 'newest')
    sort_options = {
        'newest': '-created_at',
        'oldest': 'created_at',
        'price_low': 'price',
        'price_high': '-price',
        'name': 'name',
    }
    products = products.order_by(sort_options.get(sort, '-created_at'))

    product_count = products.count()

    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'current_sort': sort,
        'product_count': product_count,
        'page_title': f'{active_category.name} — NOVA/FORM' if active_category else 'Shop — NOVA/FORM',
        'meta_description': 'Browse our curated collection of contemporary design objects, lighting, furniture, and accessories.',
    })


def product_detail(request, slug):
    """Product detail page with full info, gallery, and related products."""
    product = get_object_or_404(
        Product.objects.select_related('category'), slug=slug
    )

    related = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).select_related('category')[:4]

    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related,
        'page_title': f'{product.name} — NOVA/FORM',
        'meta_description': product.short_description or product.description[:160],
    })


def about(request):
    """About page with brand story."""
    return render(request, 'about.html', {
        'page_title': 'About — NOVA/FORM',
        'meta_description': 'We design objects that age well. Learn about the design philosophy, materials, and craftsmanship behind NOVA/FORM.',
    })


def search(request):
    """Product search."""
    query = request.GET.get('q', '').strip()
    products = []
    product_count = 0

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query) |
            Q(category__name__icontains=query)
        ).select_related('category').distinct()
        product_count = products.count()

    return render(request, 'search.html', {
        'query': query,
        'products': products,
        'product_count': product_count,
        'page_title': f'Search: {query} — NOVA/FORM' if query else 'Search — NOVA/FORM',
        'meta_description': f'Search results for "{query}" at NOVA/FORM.' if query else 'Search our collection of contemporary design objects.',
    })


# ─── CART ──────────────────────────────────────────────────────

def cart_page(request):
    """Full cart page (mobile fallback / standalone)."""
    cart = CartService(request)
    return render(request, 'cart.html', {
        'cart_items_list': cart.get_items(),
        'subtotal': cart.get_subtotal(),
        'shipping': cart.get_shipping(),
        'total': cart.get_total(),
        'is_empty': cart.is_empty(),
        'page_title': 'Bag — NOVA/FORM',
    })


@require_POST
def cart_add(request):
    """Add product to cart. Supports AJAX and form POST."""
    cart = CartService(request)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))

    success, message = cart.add(product_id, quantity)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items = cart.get_items()
        return JsonResponse({
            'success': success,
            'message': message,
            'cart_total_items': cart.get_total_items(),
            'cart_subtotal': str(cart.get_subtotal()),
            'cart_shipping': str(cart.get_shipping()),
            'cart_total': str(cart.get_total()),
            'cart_items': [
                {
                    'id': item['product'].id,
                    'name': item['product'].name,
                    'price': str(item['product'].price),
                    'quantity': item['quantity'],
                    'line_total': str(item['line_total']),
                    'image': item['product'].image,
                    'slug': item['product'].slug,
                    'category': item['product'].category.name if item['product'].category else '',
                    'stock': item['product'].stock_quantity,
                }
                for item in items
            ],
        })

    return redirect('store:cart')


@require_POST
def cart_remove(request):
    """Remove product from cart."""
    cart = CartService(request)
    product_id = request.POST.get('product_id')
    success, message = cart.remove(product_id)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items = cart.get_items()
        return JsonResponse({
            'success': success,
            'message': message,
            'cart_total_items': cart.get_total_items(),
            'cart_subtotal': str(cart.get_subtotal()),
            'cart_shipping': str(cart.get_shipping()),
            'cart_total': str(cart.get_total()),
            'cart_items': [
                {
                    'id': item['product'].id,
                    'name': item['product'].name,
                    'price': str(item['product'].price),
                    'quantity': item['quantity'],
                    'line_total': str(item['line_total']),
                    'image': item['product'].image,
                    'slug': item['product'].slug,
                    'category': item['product'].category.name if item['product'].category else '',
                    'stock': item['product'].stock_quantity,
                }
                for item in items
            ],
        })

    return redirect('store:cart')


@require_POST
def cart_update(request):
    """Update product quantity in cart."""
    cart = CartService(request)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    success, message = cart.update_quantity(product_id, quantity)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        items = cart.get_items()
        return JsonResponse({
            'success': success,
            'message': message,
            'cart_total_items': cart.get_total_items(),
            'cart_subtotal': str(cart.get_subtotal()),
            'cart_shipping': str(cart.get_shipping()),
            'cart_total': str(cart.get_total()),
            'cart_items': [
                {
                    'id': item['product'].id,
                    'name': item['product'].name,
                    'price': str(item['product'].price),
                    'quantity': item['quantity'],
                    'line_total': str(item['line_total']),
                    'image': item['product'].image,
                    'slug': item['product'].slug,
                    'category': item['product'].category.name if item['product'].category else '',
                    'stock': item['product'].stock_quantity,
                }
                for item in items
            ],
        })

    return redirect('store:cart')


# ─── AUTHENTICATION ───────────────────────────────────────────

def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('store:account')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            next_url = request.GET.get('next', 'store:account')
            return redirect(next_url)
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {
        'form': form,
        'page_title': 'Create Account — NOVA/FORM',
    })


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('store:account')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form,
        'page_title': 'Sign In — NOVA/FORM',
    })


def logout_view(request):
    """User logout."""
    logout(request)
    return redirect('store:home')


# ─── CHECKOUT & ORDERS ────────────────────────────────────────

@login_required
def checkout(request):
    """Checkout page with shipping form and order summary."""
    cart = CartService(request)

    if cart.is_empty():
        return redirect('store:shop')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order, error = OrderService.create_order(
                user=request.user,
                cart_service=cart,
                checkout_data=form.cleaned_data,
            )
            if order:
                return redirect('store:order_success', order_number=order.order_number)
            else:
                form.add_error(None, error)
    else:
        # Pre-fill form with user data
        initial = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'email': request.user.email,
        }
        form = CheckoutForm(initial=initial)

    items = cart.get_items()
    return render(request, 'checkout.html', {
        'form': form,
        'checkout_items': items,
        'subtotal': cart.get_subtotal(),
        'shipping': cart.get_shipping(),
        'total': cart.get_total(),
        'page_title': 'Checkout — NOVA/FORM',
    })


@login_required
def order_success(request, order_number):
    """Order confirmation page."""
    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        order_number=order_number,
        user=request.user,
    )
    return render(request, 'order_success.html', {
        'order': order,
        'page_title': f'Order Confirmed — NOVA/FORM',
    })


# ─── ACCOUNT ──────────────────────────────────────────────────

@login_required
def account(request):
    """User account dashboard."""
    orders = Order.objects.filter(user=request.user).prefetch_related('items')[:10]
    return render(request, 'account.html', {
        'orders': orders,
        'page_title': 'Account — NOVA/FORM',
    })


@login_required
def order_detail(request, order_number):
    """Order detail view."""
    order = get_object_or_404(
        Order.objects.prefetch_related('items'),
        order_number=order_number,
        user=request.user,
    )
    return render(request, 'order_detail.html', {
        'order': order,
        'page_title': f'Order {order.order_number} — NOVA/FORM',
    })


# ─── ERROR PAGES ──────────────────────────────────────────────

def custom_404(request, exception):
    """Custom 404 page."""
    return render(request, '404.html', {
        'page_title': 'Page Not Found — NOVA/FORM',
    }, status=404)
