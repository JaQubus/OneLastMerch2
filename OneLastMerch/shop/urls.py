from django.urls import path
from .views import main, shop_filters


urlpatterns = [
    path("", main, name="shop_main"),
    path("filters/", shop_filters, name="shop_filters"),
]
