from django.urls import path
from .views import FacturaView, VentaView

urlpatterns = [
    path('ventas/', FacturaView.as_view(), name='ventas-lista'),  # Lista de ventas
    path('ventas/crear/', VentaView.as_view(), name='venta'),  # Nueva venta
]
