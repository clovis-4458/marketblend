from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from products import views  # your app

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),

    # Main Navigation
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),

    # Category Route
    path('shop/category/<int:category_id>/', views.shop_by_category, name='shop_by_category'),

    # Product Details
    path('shop/<int:product_id>/', views.shop_details, name='shop_details'),

    # Pages
    path('pages/', views.pages, name='pages'),

    # Blog
    path('blog/', views.blog, name='blog'),
    path('blog/details/<int:blog_id>/', views.blog_details, name='blog_details'),

    # Contact
    path('contact/', views.contact, name='contact'),

    # Cart & Checkout
    path('cart/', views.shopping_cart, name='shopping_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # ✉️ Newsletter Subscribe Route (NEW)
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]

# Serve Media Files in Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
