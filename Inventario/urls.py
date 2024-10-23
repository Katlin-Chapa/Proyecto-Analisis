from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('inventario/', views.StockListView.as_view(), name='inventario'),
   # path('new', views.StockCreateView.as_view(), name='new-stock'),
    #path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    #path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)