from django.urls import path
from .views import (
    InventarioInicio,
    ProductoListView,
    ProductoDetailView,
    ModificarStockView,
    ProductoCreateView,
    CategoriaListView, 
    CategoriaCreateView,


    CargaManualView

)

urlpatterns = [
    path('inventario/', InventarioInicio.as_view(), name='inventario'), 
    path('carga/', CargaManualView.as_view(), name='carga-manual'),

    path('productos/', ProductoListView.as_view(), name='productos-lista'),  
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detalle'), 
    path('productos/<int:pk>/modificar_stock/', ModificarStockView.as_view(), name='modificar-stock'),  
    path('productos/agregar/', ProductoCreateView.as_view(), name='agregar-producto'),  
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/agregar/', CategoriaCreateView.as_view(), name='agregar-categoria'),
    
    
]
