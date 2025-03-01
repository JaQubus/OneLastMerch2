from .models import Cart, CartItem
from django.db.models import Sum

def cart_item_count(request):
    """
    A context processor to get the total number of items in the user's cart.
    It works for both authenticated and non-authenticated users.
    """
    total_items = 0
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Generate a session key if none exists
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    
    # Get the total number of items in the cart
    total_items = cart.items.aggregate(total_items=Sum('quantity'))['total_items'] or 0
    
    return {'cart_item_count': total_items}
