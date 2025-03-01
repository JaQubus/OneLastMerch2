from django.urls import path
from .views import main, shop_filters, show_image


urlpatterns = [
    path("", main, name="shop_main"),
    path("filters/", shop_filters, name="shop_filters"),
    path('item/<int:item_id>/', show_image, name='show_image'),
]
