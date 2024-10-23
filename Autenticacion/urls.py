from django.urls import path
from .views import InicioPersonalizado, UsuarioInicioVista, CustomPasswordResetView, SupportView  # Asegúrate de importar SupportView correctamente
from django.contrib.auth.views import LogoutView, PasswordResetDoneView

urlpatterns = [
    path('login/', UsuarioInicioVista.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/login/', InicioPersonalizado.as_view(), name='custom_login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('support/', SupportView.as_view(), name='support'),  # Asegúrate de que estás usando SupportView
]
