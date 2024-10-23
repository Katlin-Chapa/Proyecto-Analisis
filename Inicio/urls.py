from django.urls import path
from . import views

urlpatterns = [
    path('', views.InicioVista.as_view(), name='inicio'),
    path('acerca/', views.AcercaVista.as_view(), name='acerca')
]