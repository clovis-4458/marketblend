from django.db import models
from django.core.validators import validate_email
from django.core.mail import send_mail


# 🏷️ Product Categories
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# 🛒 Products
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)  # NEW
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest products first

    def __str__(self):
        return self.name


# 📰 Blog Posts
class Blog(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    content = models.TextField()
    author = models.CharField(max_length=100, default="Admin")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # newest first

    def __str__(self):
        return self.title


# ✉️ Newsletter Subscribers (FULLY UPGRADED)
class Subscriber(models.Model):
    email = models.EmailField(unique=True, validators=[validate_email])
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subscribed_at']
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return self.email

    # Auto-send thank-you email after subscription
    def save(self, *args, **kwargs):
        new = self.pk is None  # Detect new subscriber
        super().save(*args, **kwargs)
        if new:
            try:
                send_mail(
                    "Thank you for subscribing!",
                    "You have successfully joined our newsletter.",
                    "noreply@mtechithub.com",  # use your domain / SMTP later
                    [self.email],
                    fail_silently=True,
                )
            except:
                pass  # Avoid errors if email fails
