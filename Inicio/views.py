from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
def inicio_view(request):
    return render(request, 'inicio.html')

class SesionView(LoginRequiredMixin, TemplateView):
    template_name = 'sesion.html'
    login_url = reverse_lazy('login')

class AcercaView(TemplateView):
    template_name = 'acerca.html'

class ContactoView(TemplateView):
    template_name = 'contacto.html'