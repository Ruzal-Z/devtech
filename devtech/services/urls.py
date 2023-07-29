from django.urls import path

from .views import services_main, password_generator

urlpatterns = [
    path('', services_main, name='services_main'),
    path('password_generator/', password_generator, name='password_generator'),
]
