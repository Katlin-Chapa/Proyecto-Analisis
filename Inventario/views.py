from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from .models import Producto, MovimientoInventario
from django.urls import reverse_lazy
from .forms import ProductoForm
from .models import Categoria
from .forms import CategoriaForm

# Vista para listar categorías
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'categorias.html'

# Vista para crear una nueva categoría
class CategoriaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'agregar_categoria.html'
    success_url = reverse_lazy('categoria-list')  # Redirigir a la lista de categorías después de agregar

    def test_func(self):
        return self.request.user.is_staff

# Vista para mostrar los productos según el rol del usuario
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos.html'  # Un solo template para ambos roles

    def get_queryset(self):
        # Devuelve todos los productos
        return Producto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = self.request.user.is_staff  # Añadir el rol del usuario al contexto
        return context

# Vista para el detalle del producto
class ProductoDetailView(LoginRequiredMixin, DetailView):
    model = Producto
    template_name = 'producto_detalle.html'

# Vista para modificar el stock del producto y solicitar el número de documento
class ModificarStockView(LoginRequiredMixin, UpdateView):
    model = Producto
    fields = ['stock_actual']
    template_name = 'modificar_stock.html'  # Template para modificar stock
    success_url = reverse_lazy('productos')  # Redirigir a la lista de productos después de la modificación

    def post(self, request, *args, **kwargs):
        producto = self.get_object()
        numero_documento = request.POST.get('numero_documento', None)
        cantidad = request.POST.get('stock_actual', None)

        if not numero_documento:
            return render(request, self.template_name, {'form': self.get_form(), 'error': "Debe proporcionar un número de documento."})

        # Crear el movimiento de inventario
        MovimientoInventario.objects.create(
            producto=producto,
            cantidad=int(cantidad) - producto.stock_actual,
            tipo='entrada' if int(cantidad) > producto.stock_actual else 'salida',
            usuario=request.user,
            numero_documento=numero_documento
        )

        # Actualizar el stock del producto
        producto.stock_actual = cantidad
        producto.save()

        return redirect(self.success_url)

class ProductoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'agregar_producto.html'
    success_url = reverse_lazy('productos')  # Redirigir a la lista de productos después de agregar

    def test_func(self):
        return self.request.user.is_staff  # Solo permitir que los administradores accedan