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

from django.http import JsonResponse
from .models import Stock

def obtener_lotes(request, stock_id):
    stock = Stock.objects.filter(id=stock_id).first()
    if stock:
        lotes = stock.lotes.all()
        data = [{'numero_documento': lote.numero_documento, 'fecha_vencimiento': lote.fecha_vencimiento} for lote in lotes]
        return JsonResponse({'lotes': data})
    return JsonResponse({'lotes': []})


from django.shortcuts import render, redirect
from .models import Categoria, Stock

def agregar_categoria_producto(request):
    if request.method == 'POST':
        if 'nombre_categoria' in request.POST:
            # Procesar formulario de categoría
            nombre_categoria = request.POST.get('nombre_categoria')
            Categoria.objects.create(nombre=nombre_categoria)
            return redirect('agregar')  # Redirigir después de agregar
        elif 'nombre_producto' in request.POST:
            # Procesar formulario de producto
            nombre_producto = request.POST.get('nombre_producto')
            cantidad = request.POST.get('cantidad')
            precio = request.POST.get('precio')
            dosis = request.POST.get('dosis')
            numero_documento = request.POST.get('numero_documento')
            fecha_vencimiento = request.POST.get('fecha_vencimiento')
            categoria = Categoria.objects.get(id=request.POST.get('categoria'))
            imagen = request.FILES.get('imagen')

            Stock.objects.create(
                nombre=nombre_producto,
                cantidad=cantidad,
                precio=precio,
                dosis=dosis,
                numero_documento=numero_documento,
                fecha_vencimiento=fecha_vencimiento,
                categoria=categoria,
                imagen=imagen
            )
            return redirect('agregar')  # Redirigir después de agregar

    categorias = Categoria.objects.all()
    return render(request, 'agregar.html', {'categorias': categorias})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Stock, Categoria

def modificar_producto(request, id):
    stock = get_object_or_404(Stock, id=id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.POST.get('nombre')
        cantidad = request.POST.get('cantidad')
        precio = request.POST.get('precio')
        dosis = request.POST.get('dosis')
        categoria_id = request.POST.get('categoria')
        imagen = request.FILES.get('imagen')

        # Actualizar solo los campos que se pueden modificar
        stock.nombre = nombre
        stock.cantidad = cantidad
        stock.precio = precio
        stock.dosis = dosis
        stock.categoria_id = categoria_id

        # Si se proporciona una nueva imagen, actualizarla
        if imagen:
            stock.imagen = imagen

        # Guardar los cambios en el modelo
        stock.save()

        # Redirigir a la lista de inventario u otra vista
        return redirect('inventario')  # Cambia esto según tu URL de lista de inventario

    context = {
        'stock': stock,
        'categorias': categorias,
    }
    return render(request, 'modificar.html', context)

# views.py
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Stock  # Asegúrate de importar tu modelo
from django.contrib.auth.decorators import login_required

@login_required
def eliminar_producto(request, stock_id):
    producto = get_object_or_404(Stock, id=stock_id)
    producto.delete()
    return redirect(reverse('inventario'))  # Redirige a la página de inventario

