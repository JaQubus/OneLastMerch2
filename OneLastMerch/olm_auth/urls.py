from django.urls import path
from .views import olm_register, olm_login, olm_logout

urlpatterns = [
    path("register/", olm_register, name="register"),
    path("login/", olm_login, name="login"),
    path("logout/", olm_logout, name="logout"),
]
