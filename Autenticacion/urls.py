from django.urls import path
from .views import InicioPersonalizado, UsuarioInicioVista
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', UsuarioInicioVista.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/login/', InicioPersonalizado.as_view(), name='custom_login'),
]
