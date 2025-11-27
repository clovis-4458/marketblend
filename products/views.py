from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

from .models import Product, Category, Blog, Subscriber  # ✅ added Subscriber model


# ==============================
# 🏠 Home Page
# ==============================
def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(available=True, is_featured=True)[:12]  # limit for slider
    products = Product.objects.filter(available=True)

    return render(request, "products/home.html", {
        "products": products,
        "featured_products": featured_products,
        "categories": categories,
    })


# ==============================
# 🛒 Shop Page (Search + Category)
# ==============================
def shop(request):
    categories = Category.objects.all()
    query = request.GET.get("q", "")
    category_id = request.GET.get("category")

    products = Product.objects.filter(available=True)

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category_id and category_id.isdigit():
        products = products.filter(category_id=int(category_id))

    return render(request, "products/shop.html", {
        "products": products,
        "categories": categories,
        "query": query,
        "selected_category": int(category_id) if category_id else None,
    })


# ==============================
# 🏷️ Shop by Category
# ==============================
def shop_by_category(request, category_id):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, available=True)

    return render(request, "products/shop.html", {
        "products": products,
        "categories": categories,
        "selected_category": category.id,
    })


# ==============================
# 📄 General Pages
# ==============================
def pages(request):
    categories = Category.objects.all()
    return render(request, "products/pages.html", {"categories": categories})


# ==============================
# 📰 Blog Page
# ==============================
def blog(request):
    categories = Category.objects.all()
    blogs = Blog.objects.all()

    return render(request, "products/blog.html", {
        "blogs": blogs,
        "categories": categories,
    })


# ==============================
# 🧾 Blog Details Page
# ==============================
def blog_details(request, blog_id):
    categories = Category.objects.all()
    blog_post = get_object_or_404(Blog, id=blog_id)

    return render(request, "products/blog_details.html", {
        "blog": blog_post,
        "categories": categories,
    })


# ==============================
# ✉️ Contact Page
# ==============================
def contact(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # You could also send contact email here if needed

        messages.success(request, "Your message was sent successfully!")
        return redirect("contact")

    return render(request, "products/contact.html", {"categories": categories})


# ==============================
# 🔍 Product Details Page
# ==============================
def shop_details(request, product_id):
    categories = Category.objects.all()
    product = get_object_or_404(Product, id=product_id, available=True)

    return render(request, "products/product_details.html", {
        "product": product,
        "categories": categories,
    })


# ==============================
# 🛍️ Shopping Cart Page
# ==============================
def shopping_cart(request):
    categories = Category.objects.all()
    return render(request, "products/shopping_cart.html", {"categories": categories})


# ==============================
# 💳 Checkout Page
# ==============================
def checkout(request):
    categories = Category.objects.all()
    return render(request, "cart/checkout.html", {"categories": categories})


# ==============================
# ✉️ Newsletter Subscribe
# ==============================
def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")

        # empty email
        if not email:
            messages.error(request, "Please enter an email address.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # already exists
        if Subscriber.objects.filter(email=email).exists():
            messages.warning(request, "This email is already subscribed.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # save email
        Subscriber.objects.create(email=email)

        # ✅ Send thank-you email
        subject = "Thank You for Subscribing!"
        message = (
            f"Hello,\n\n"
            f"Thank you for subscribing to our newsletter. "
            f"You will now receive updates about new products and offers.\n\n"
            f"Best regards,\n"
            f"Market Blend Team"
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        except Exception as e:
            print("Email sending failed:", e)  # replace with proper logging in production

        messages.success(request, "You subscribed successfully! A confirmation email has been sent to you.")

        return redirect(request.META.get("HTTP_REFERER", "/"))

    return redirect("home")
