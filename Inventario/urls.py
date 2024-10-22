from django.urls import path
from .views import (
    ProductoListView,
    ProductoDetailView,
    ModificarStockView,
    ProductoCreateView,
    CategoriaListView, 
    CategoriaCreateView
)

urlpatterns = [
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/agregar/', CategoriaCreateView.as_view(), name='agregar-categoria'),
    path('productos/', ProductoListView.as_view(), name='productos'),  # Vista para listar productos
    path('productos/<int:pk>/', ProductoDetailView.as_view(), name='producto-detalle'),  # Vista para detalle de producto
    path('productos/<int:pk>/modificar_stock/', ModificarStockView.as_view(), name='modificar-stock'),  # Vista para modificar stock
    path('productos/agregar/', ProductoCreateView.as_view(), name='agregar-producto'),  # Nueva URL para agregar productos
]
