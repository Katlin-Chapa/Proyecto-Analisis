from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    View,
    CreateView, 
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .models import Stock
from .forms import StockForm
from django_filters.views import FilterView
from .filters import StockFilter


class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(es_eliminado=False)
    template_name = 'inventario.html'

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Stock, Lote
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json

class CargarProductosAnualmente(ListView):
    model = Stock
    template_name = 'cargar_productos.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Stock.objects.filter(nombre__icontains=query, es_eliminado=False)
        return Stock.objects.filter(es_eliminado=False)

from django.shortcuts import render, redirect
from .forms import LoteForm
from .models import Stock

def crear_lote(request):
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            # Asignar el stock desde el formulario
            stock_id = request.POST.get('stock')
            lote.stock = Stock.objects.get(id=stock_id)
            # Actualiza la cantidad del stock
            stock = lote.stock
            stock.cantidad += lote.cantidad  # Actualiza la cantidad
            stock.save()  # Guarda el stock actualizado
            lote.save()  # Guarda el nuevo lote
            return redirect('cargar-productos')  # Cambia esto por tu URL de éxito
    else:
        form = LoteForm()
    
    return render(request, 'crear_lote.html', {'form': form})

