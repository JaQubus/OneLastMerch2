from django.urls import path
from .views import about_us, account
from .wheel import spin_result, spin_wheel, spin_wheel_api

urlpatterns = [
    path('account/', account, name="account"),
    path('about-us/', about_us, name="about-us"),
    path('spin/', spin_wheel, name='spin_wheel'),
    path('spin-api/', spin_wheel_api, name='spin_wheel_api'),
    path('result/', spin_result, name='spin_result'),
]
