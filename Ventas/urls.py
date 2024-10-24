from django.urls import path
from . import views

urlpatterns = [
    path('ventas/', views.FacturaView.as_view(), name='lista-ventas'),
    path('venta/new', views.CrearFacturaView.as_view(), name='nueva-venta'),
    path("factura/<billno>", views.FacturaDetalleView.as_view(), name="factura"),
]