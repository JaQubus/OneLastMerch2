from django.urls import path
from .views import main, shop_filters, show_image, add_to_cart, view_cart, remove_from_cart, update_cart_item_quantity

urlpatterns = [
    path("", main, name="shop_main"),
    path("filters/", shop_filters, name="shop_filters"),
    path("item/<int:item_id>/", show_image, name="show_image"),
    
    # Cart URLs
    path("cart/", view_cart, name="view_cart"),
    path("cart/add/<int:item_id>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:cart_item_id>/", remove_from_cart, name="remove_from_cart"),
    path('cart/update/<int:item_id>/', update_cart_item_quantity, name='update_cart_item_quantity'),
]
