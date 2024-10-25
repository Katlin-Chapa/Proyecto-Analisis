from django.urls import path
from .views import gestionar_usuarios, eliminar_usuario

urlpatterns = [
    path('gestionar-usuarios/', gestionar_usuarios, name='gestionar_usuarios'),
    path('eliminar-usuario/<int:user_id>/', eliminar_usuario, name='eliminar_usuario'),
]
