from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from products import views  # Import your main site views

urlpatterns = [
    # ⚙️ Admin Panel
    path('admin/', admin.site.urls),

    # 🏠 Main site navigation
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/category/<int:category_id>/', views.shop_by_category, name='shop_by_category'),
    path('shop/<int:product_id>/', views.shop_details, name='shop_details'),
    path('pages/', views.pages, name='pages'),

    # ⭐ Newsletter Subscribe Route (ADDED)
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),

    # 📖 Blog (Dynamic Blog App)
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),

    # 📞 Contact
    path('contact/', views.contact, name='contact'),

    # 🛒 Cart system
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),

    # 👤 User Authentication
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
]

# 📸 Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
