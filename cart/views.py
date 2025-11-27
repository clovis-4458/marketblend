from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.urls import reverse_lazy
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .utils import add_to_session_cart

User = get_user_model()


# =========================
# LOGIN VIEW
# =========================
def index(request):
    """
    Login view with 'next' support.
    """
    next_url = request.GET.get("next") or request.POST.get("next") or reverse_lazy('shop')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html", {"next": next_url})


# =========================
# REGISTER VIEW
# =========================
def register_view(request):
    """
    Register view with 'next' support.
    """
    next_url = request.GET.get("next") or request.POST.get("next") or reverse_lazy('shop')

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            messages.success(request, f"Welcome {username}! Your account has been created.")
            return redirect(next_url)

    return render(request, "register.html", {"next": next_url})


# =========================
# LOGOUT VIEW
# =========================
@login_required
def logout_view(request):
    """
    Logout the current user and redirect to the shop or login page.
    """
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('shop')  # or 'login' if you prefer


# =========================
# VIEW CART
# =========================
def view_cart(request):
    cart_items = []
    total = 0

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        for item in items:
            subtotal = item.quantity * item.product.price
            cart_items.append({
                'id': item.id,
                'product': item.product,
                'quantity': item.quantity,
                'subtotal': subtotal,
            })
            total += subtotal
    else:
        session_cart = request.session.get('cart', {})
        for pid, quantity in session_cart.items():
            try:
                product = Product.objects.get(id=int(pid))
                subtotal = int(quantity) * product.price
                cart_items.append({
                    'id': int(pid),
                    'product': product,
                    'quantity': int(quantity),
                    'subtotal': subtotal,
                })
                total += subtotal
            except Product.DoesNotExist:
                continue

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
    })


# =========================
# ADD TO CART
# =========================
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += 1
            messages.info(request, f"Updated {product.name} quantity in your cart.")
        else:
            messages.success(request, f"Added {product.name} to your cart.")
        item.save()
    else:
        add_to_session_cart(request, product_id, 1)
        messages.success(request, f"{product.name} added to cart (guest mode).")
        request.session.modified = True

    return redirect(request.META.get("HTTP_REFERER", 'cart:view_cart'))


# =========================
# REMOVE FROM CART
# =========================
def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        CartItem.objects.filter(id=item_id).delete()
    else:
        session_cart = request.session.get('cart', {})
        session_cart.pop(str(item_id), None)
        request.session['cart'] = session_cart
        request.session.modified = True
    return redirect('cart:view_cart')


# =========================
# CLEAR CART
# =========================
def clear_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.filter(cart=cart).delete()
    else:
        request.session['cart'] = {}
        request.session.modified = True

    messages.warning(request, "Your cart has been cleared.")
    return redirect('cart:view_cart')


# =========================
# CHECKOUT
# =========================
@login_required(login_url=reverse_lazy('accounts:index'))
def checkout(request):
    """
    Checkout view — ensures login and pre-fills user info.
    """
    cart_items = []
    total = 0

    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('shop')

    for item in items:
        subtotal = item.quantity * item.product.price
        cart_items.append({
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })
        total += subtotal

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment')

        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total=total,
            status='pending'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                subtotal=item['subtotal']
            )

        CartItem.objects.filter(cart=cart).delete()
        messages.success(request, "✅ Your order has been placed successfully!")
        return redirect('shop')

    initial_data = {
        'name': request.user.get_full_name() or request.user.username,
        'email': request.user.email,
    }

    return render(request, 'cart/checkout.html', {
        'cart_items': cart_items,
        'cart_total': total,
        'initial_data': initial_data,
    })
