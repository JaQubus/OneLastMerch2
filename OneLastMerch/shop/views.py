from django.shortcuts import render
from .models import Item
from .forms import FilterForm
from django.db.models import QuerySet
from typing import Optional, Dict, Any

def get_items(filters: Optional[list] = None):
    # Fetch all items from the database and only select specific fields
    items = Item.objects.all().values("title", "price", "image")
    # If filter is provided, filter by the tags
    if filters:
        items = items.filter(tag__in=filters)
    
    # Convert the result into a list of dictionaries and return
    return items

def main(request):
    # Get all items
    items = get_items()  # Default, no filter
    form = FilterForm()  # Create a form instance
    return render(request, "shop/shop.html", {"items": items, "form": form})

def shop_filters(request):
    # Handling POST request with selected tags
    if request.method == "POST" and request.POST.getlist("tags"):
        tags = request.POST.getlist("tags")  # Get selected tags from form
        form = FilterForm(request.POST)  # Create a form instance with POST data
        # Filter items based on selected tags
        items = get_items(tags)  # Filter items by tags
    else:
        # If no tags selected, just get all items
        items = get_items()
        form = FilterForm()  # Empty form
    return render(request, "shop/shop.html", {"items": items, "form": form})
