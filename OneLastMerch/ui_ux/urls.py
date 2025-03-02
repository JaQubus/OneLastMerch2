from django.urls import path
from .views import about_us, account
from .wheel import spin_wheel_ui, spin_wheel_api

urlpatterns = [
    path('account/', account, name="account"),
    path('about-us/', about_us, name="about-us"),
    path('spin-wheel/', spin_wheel_ui, name='spin_wheel_ui'),
    path('spin-wheel-api/', spin_wheel_api, name='spin_wheel_api'),
]
