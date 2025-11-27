from django.contrib import admin
from .models import Product, Category, Blog, Subscriber


# 🏷️ Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# 🛒 Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'available', 'is_featured', 'created_at')
    list_filter = ('available', 'is_featured', 'category')
    search_fields = ('name', 'description')
    ordering = ('-created_at',)


# 📰 Blog Admin
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    search_fields = ('title', 'content', 'author')
    ordering = ('-created_at',)


# ✉️ Newsletter Subscribers Admin
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    ordering = ('-subscribed_at',)
