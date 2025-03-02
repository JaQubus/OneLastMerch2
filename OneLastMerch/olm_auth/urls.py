from django.urls import path
from .views import olm_register, olm_login, olm_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("register/", olm_register, name="register"),
    path("login/", olm_login, name="login"),
    path("logout/", olm_logout, name="logout"),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='ui_ux/change_password.html'), name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='ui_ux/change_password_done.html'), name='password_change_done'),
]
