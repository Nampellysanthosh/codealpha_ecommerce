from .models import Product

def cart_context(request):
    """
    Context processor to inject shopping cart summary (item count & total)
    across all templates in the store.
    """
    cart = request.session.get('cart', {})
    cart_total_count = 0
    
    for qty in cart.values():
        if isinstance(qty, int):
            cart_total_count += qty

    return {
        'cart_total_count': cart_total_count,
    }
