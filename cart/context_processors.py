from .utils import cart_summary as get_cart_summary

def cart_summary(request):
    """
    Context processor to add cart_count and cart_total
    to every template for both logged-in and guest users.
    """
    try:
        summary = cart_summary_helper(request)
    except Exception:
        # If any error occurs (e.g., DB issue), return default values
        summary = {
            "cart_count": 0,
            "cart_total": 0
        }
    return summary


def cart_summary_helper(request):
    """
    Internal helper to call utils.cart_summary.
    Avoids circular import issues and naming conflicts.
    """
    return get_cart_summary(request)
