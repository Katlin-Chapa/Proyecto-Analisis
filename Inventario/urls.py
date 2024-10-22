from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('carga/', views.carga_producto, name='carga_producto'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/crear/', views.crear_producto, name='crear_producto'),
    path('producto/editar/<int:producto_id>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    
]

if settings.DEBUG:  # Solo sirve archivos de medios en modo de depuración
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)