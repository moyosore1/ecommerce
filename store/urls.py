from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='Store-home'),
    path('category/products/<str:pk>', views.category_products, name='Store-category_products'),
    path('cart/', views.cart, name='Store-cart'),
    path('checkout/', views.checkout, name='Store-checkout'),
    path('update-cart/', views.update_cart, name='Update-cart'),
    path('shipping/', views.shipping, name='Store-shipping'),
    path('wishlist/', views.wishlist, name='Store-wishlist'),
    path('product-details/<str:pk>', views.product_details, name='Product_details'),
    path('add-to-wishlist/<str:pk>', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<str:pk>', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('move_to_cart/<str:pk>', views.move_to_cart, name='move_to_cart'),
    path('search/', views.search_products, name='Search-product'),
    path('help/', views.help_customers, name='Store-help'),
    path('contact/', views.contact_us, name='Store-contactus'),
    path('myaccount/', views.account_details, name='account-info'),
]
