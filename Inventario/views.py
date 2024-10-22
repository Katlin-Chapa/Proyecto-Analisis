from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import CrearProductoForm, CargaProductoForm
from django.contrib.auth.decorators import login_required

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = CrearProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = CrearProductoForm()
    
    return render(request, 'crear_producto.html', {'form': form})

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

@login_required
def carga_producto(request):
    if request.method == 'POST':
        form = CargaProductoForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            documento = form.cleaned_data['documento']  # Aquí puedes usar el documento según sea necesario
            
            # Actualizar la cantidad del producto
            producto.cantidad += cantidad
            producto.save()
            return redirect('lista_productos')
    else:
        form = CargaProductoForm()
    
    return render(request, 'carga_producto.html', {'form': form})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    if request.method == 'POST':
        form = CrearProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = CrearProductoForm(instance=producto)
    
    return render(request, 'crear_producto.html', {'form': form})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    producto.delete()
    return redirect('lista_productos')
