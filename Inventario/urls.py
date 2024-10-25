from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    StockListView, 
    CargarProductosAnualmente, 
    crear_lote, 
    agregar_categoria_producto, 
    modificar_producto, 
    eliminar_producto,
    reportes_view,  # Asegúrate de que esta vista esté definida en tu views.py
)

urlpatterns = [
    path('inventario/', views.StockListView.as_view(), name='inventario'),
    path('cargar/', views.CargarProductosAnualmente.as_view(), name='cargar-productos'),  # Página para cargar productos
    path('crear-lote/', crear_lote, name='crear_lote'),
    path('agregar/', views.agregar_categoria_producto, name='agregar'),
    path('modificar/<int:id>/', views.modificar_producto, name='modificar'),
    path('eliminar/<int:stock_id>/', eliminar_producto, name='eliminar_producto'),
    
    # Rutas para generar reportes de Stock
    path('pdf/', views.generar_pdf, name='generar_pdf'),
    path('excel/', views.generar_excel, name='generar_excel'),
    
    # Rutas para generar reportes de Lote
    path('lote_pdf/', views.generar_lote_pdf, name='generar_lote_pdf'),
    path('lote_excel/', views.generar_lote_excel, name='generar_lote_excel'),
    path('reportes/', reportes_view, name='reportes'),  # Asegúrate de usar la vista correcta
]

# Configuración para servir archivos estáticos y media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
