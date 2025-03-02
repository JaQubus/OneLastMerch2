from django.urls import path
from .views import about_us, account
from .wheel import spin_wheel

urlpatterns = [
    path('account/', account, name="account"),
    path('about-us/', about_us, name="about-us"),
    path("spin-wheel/", spin_wheel, name="spin_wheel"),
]
