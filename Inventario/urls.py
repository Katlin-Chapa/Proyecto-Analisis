from django.urls import path
from . import views

urlpatterns = [
    path('carga/', views.carga_producto, name='carga_producto'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('admin/crear/', views.crear_producto, name='crear_producto'),
    path('admin/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('admin/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]
