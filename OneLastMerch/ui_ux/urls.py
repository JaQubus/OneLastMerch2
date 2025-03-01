from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account, name="account"),
    path('about-us/', views.about_us, name="about-us"),
]
