from django.urls import path
from .views import inicio_view, SesionView, AcercaView, ContactoView

urlpatterns = [
    path('', inicio_view, name='inicio'),
    path('sesion/', SesionView.as_view(), name='sesion'),
    path('acerca/', AcercaView.as_view(), name='acerca'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
]