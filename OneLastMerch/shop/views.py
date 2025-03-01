from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Cart, CartItem
from .forms import FilterForm
from typing import Optional
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def get_items(filters: Optional[list] = None):
    # Fetch all items from the database and only select specific fields
    items = Item.objects.all().values("id", "title", "price", "image")
    # If filter is provided, filter by the tags
    if filters:
        items = items.filter(tag__in=filters)
    
    # Convert the result into a list of dictionaries and return
    return items

def main(request):
    tags = request.GET.getlist("tags")  # Get tags from URL query parameters
    items = get_items(tags if tags else None)  # Fetch items with or without filters
    form = FilterForm(initial={"tags": tags})  # Pre-fill the form with selected filters
    return render(request, "shop/shop.html", {"items": items, "form": form})

def shop_filters(request):
    # Handling POST request with selected tags
    if request.method == "POST" and request.POST.getlist("tags"):
        tags = request.POST.getlist("tags")  # Get selected tags from form
        form = FilterForm(request.POST)  # Create a form instance with POST data

        items = get_items(tags)  # Filter items by tags
    else:
        # If no tags selected, just get all items
        items = get_items()
        form = FilterForm()  # Empty form
    return render(request, "shop/shop.html", {"items": items, "form": form})

def show_image(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item_dict = model_to_dict(item, fields=["id", "title", "price", "image"])  # Convert to dict
    
    # Convert image field to string (filename)
    if isinstance(item_dict["image"], str) is False:
        item_dict["image"] = str(item.image)  # Ensures it's just the filename
    
    return render(request, 'shop/image_detail.html', {'item': item_dict})

def get_cart(request):
    """Retrieve the user's cart or create one."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Generate a session key if none exists
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)

    return cart

@login_required
def add_to_cart(request, item_id):
    """Add item to cart and persist it in the database."""
    cart = get_cart(request)
    item = get_object_or_404(Item, id=item_id)
    
    # Check if item already exists in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Return response for AJAX or redirect
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"message": "Item added to cart!"})
    
    return redirect("view_cart")

from django.shortcuts import render
from .models import Cart, CartItem
from django.forms.models import model_to_dict

@login_required
def view_cart(request):
    """Display cart items as dictionaries."""
    cart = get_cart(request)  # Assume get_cart function returns the current cart
    cart_items = cart.items.select_related("item")  # Get cart items and related items

    # Convert cart items into a list of dictionaries
    cart_items_dict = []
    for cart_item in cart_items:
        item_dict = model_to_dict(cart_item.item, fields=["id", "title", "price", "image"])  # Convert the item to a dict
        
        # Include the quantity of the item in the cart
        item_dict['quantity'] = cart_item.quantity
        
        # Convert image field to string (filename)
        if isinstance(item_dict["image"], str) is False:
            item_dict["image"] = str(cart_item.item.image)  # Ensures it's just the filename
        
        cart_items_dict.append(item_dict)

    return render(request, "shop/cart.html", {"cart_items": cart_items_dict})

@login_required
def remove_from_cart(request, cart_item_id):
    # Get the CartItem object to remove
    cart_item = get_object_or_404(CartItem, item_id=cart_item_id)

    # Remove the item from the cart
    cart_item.delete()

    # Redirect to the cart page after removal
    return redirect('view_cart')

@login_required
def update_cart_item_quantity(request, item_id):
    # Fetch the cart item for the logged-in user's cart
    cart_item = get_object_or_404(CartItem, item_id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        
        cart_item.save()
    
    return redirect('view_cart')