from django.urls import path
from . import views

# ✅ Namespace for the blog app
app_name = 'blog'

urlpatterns = [
    # 📝 Blog list page
    path('', views.blog_list, name='list'),

    # 📝 Blog detail page (uses slug instead of ID)
    path('<slug:slug>/', views.blog_detail, name='detail'),
]
