"""
NOVA/FORM — URL Configuration
"""

from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # Public pages
    path('', views.splash, name='splash'),
    path('home/', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),

    # Cart
    path('cart/', views.cart_page, name='cart'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/remove/', views.cart_remove, name='cart_remove'),
    path('cart/update/', views.cart_update, name='cart_update'),

    # Authentication
    path('account/register/', views.register_view, name='register'),
    path('account/login/', views.login_view, name='login'),
    path('account/logout/', views.logout_view, name='logout'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmed/<str:order_number>/', views.order_success, name='order_success'),

    # Account
    path('account/', views.account, name='account'),
    path('account/order/<str:order_number>/', views.order_detail, name='order_detail'),
]
