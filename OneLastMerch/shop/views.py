from django.shortcuts import render, get_object_or_404
from .models import Item
from .forms import FilterForm
from typing import Optional
from django.forms.models import model_to_dict

def get_items(filters: Optional[list] = None):
    # Fetch all items from the database and only select specific fields
    items = Item.objects.all().values("id", "title", "price", "image")
    # If filter is provided, filter by the tags
    if filters:
        items = items.filter(tag__in=filters)
    
    # Convert the result into a list of dictionaries and return
    return items

def main(request):
    # Get all items
    items = get_items()
    form = FilterForm()  # Create a form instance
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

    print(item_dict)  # Debugging
    
    return render(request, 'shop/image_detail.html', {'item': item_dict})
