from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import StockListView, CargarProductosAnualmente, crear_lote, agregar_categoria_producto

urlpatterns = [
    path('inventario/', views.StockListView.as_view(), name='inventario'),
    path('cargar/', views.CargarProductosAnualmente.as_view(), name='cargar-productos'),  # Página para cargar productos
    path('crear-lote/', crear_lote, name='crear_lote'),
    path('agregar/', views.agregar_categoria_producto, name='agregar'),

  #  path('agregar-lote/<int:producto_id>/', AgregarLoteView.as_view(), name='agregar-lote'),  # Añadir lote a producto
  #   path('cargar/', StockListView.as_view(), name='cargar'),
   # path('agregar-lote/<int:producto_id>/', AgregarLoteView.as_view(), name='agregar_lote'),
   # path('new', views.StockCreateView.as_view(), name='new-stock'),
    #path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    #path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)