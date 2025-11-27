from products.models import Product

def add_to_session_cart(request, product_id, qty=1):
    """Store cart items for guests inside Django session."""
    cart = request.session.get("cart", {})
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + int(qty)
    request.session["cart"] = cart
    request.session.modified = True

def cart_summary(request):
    """
    Returns cart_count and cart_total.
    Works for both logged-in and guest users.
    """
    cart_count = 0
    cart_total = 0

    # Logged-in user
    if request.user.is_authenticated:
        from .models import Cart, CartItem
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart).select_related("product")
        for item in items:
            cart_count += item.quantity
            cart_total += item.quantity * item.product.price
    else:
        # Guest (session cart)
        session_cart = request.session.get("cart", {})
        for pid, qty in session_cart.items():
            try:
                product = Product.objects.get(id=int(pid))
                cart_count += int(qty)
                cart_total += int(qty) * product.price
            except Product.DoesNotExist:
                continue

    return {
        "cart_count": cart_count,
        "cart_total": cart_total,
    }
