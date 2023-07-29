from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from .views import RegisterUser, logout_user

app_name = 'users'

urlpatterns = [
    # Авторизация
    path('login/',
         LoginView.as_view(template_name='users/login.html'),
         name='login'),
    # Регистрация
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
]