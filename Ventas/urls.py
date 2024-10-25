from django.urls import path
from .views import FacturaView, VentaView, get_stock_price, GuardarVentaView

urlpatterns = [
    path('ventas/', FacturaView.as_view(), name='ventas-lista'),  # Lista de ventas
    path('ventas/crear/', VentaView.as_view(), name='venta'),  # Nueva venta
    path('api/stock/<int:stock_id>/', get_stock_price, name='get_stock_price'),
    path('efectivo/', GuardarVentaView.as_view(), name='guardar_venta'),

]
