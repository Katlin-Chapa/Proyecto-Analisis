from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from .models import Producto, MovimientoInventario, Categoria
from django.urls import reverse_lazy
from .forms import ProductoForm, CategoriaForm

class InventarioInicio(LoginRequiredMixin, TemplateView):
    template_name = 'inventario_menu.html'

# Vista para listar categorías
class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'categorias.html'

# Vista para crear una nueva categoría
class CategoriaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'agregar_categoria.html'
    success_url = reverse_lazy('categoria-list')  

    def test_func(self):
        return self.request.user.is_staff

# Vista para mostrar los productos según el rol del usuario
class ProductoListView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'productos.html'  

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
    template_name = 'modificar_stock.html'  
    success_url = reverse_lazy('productos')  

def post(self, request, *args, **kwargs):
    producto = self.get_object()
    numero_documento = request.POST.get('numero_documento', None)
    cantidad = request.POST.get('stock_actual', None)

    # Validar el número de documento
    if not numero_documento:
        return render(request, self.template_name, {'form': self.get_form(), 'error': "Debe proporcionar un número de documento."})

    # Validar la cantidad
    if cantidad is None or not cantidad.isdigit():
        return render(request, self.template_name, {'form': self.get_form(), 'error': "La cantidad debe ser un número."})

    cantidad = int(cantidad)

    # Verifica si se trata de una entrada o salida
    if cantidad > producto.stock_actual:  # Se está agregando stock
        movimiento_tipo = 'entrada'
        movimiento_cantidad = cantidad - producto.stock_actual  # Se registra la diferencia
    else:  # Se está reduciendo stock
        if cantidad < producto.stock_actual:  # Solo permitimos salida si hay stock suficiente
            movimiento_tipo = 'salida'
            movimiento_cantidad = producto.stock_actual - cantidad  # Se registra la diferencia
        else:
            return render(request, self.template_name, {'form': self.get_form(), 'error': "No se puede reducir el stock al mismo valor."})

    # Crear el movimiento de inventario
    MovimientoInventario.objects.create(
        producto=producto,
        cantidad=movimiento_cantidad,
        tipo=movimiento_tipo,
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
    success_url = reverse_lazy('productos')  

    def test_func(self):
        return self.request.user.is_staff  
    






from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import render, redirect
from .models import Producto, MovimientoInventario
from django.contrib.auth.mixins import LoginRequiredMixin

class CargaManualView(LoginRequiredMixin, ListView):
    model = Producto
    template_name = 'carga_manual.html'
    context_object_name = 'productos'
    paginate_by = 10  # Número de productos por página

    def get_queryset(self):
        # Filtrar por nombre o categoría si hay búsqueda
        busqueda = self.request.GET.get('busqueda', '')
        queryset = Producto.objects.all()

        if busqueda:
            queryset = queryset.filter(
                Q(nombre__icontains=busqueda) | 
                Q(categoria__nombre__icontains=busqueda)
            )
        
        return queryset.order_by('nombre')  # Ordenar alfabéticamente

    def post(self, request, *args, **kwargs):
        # Obtener datos del formulario
        producto_id = request.POST.get('producto_id')
        cantidad = request.POST.get('cantidad')
        numero_documento = request.POST.get('numero_documento')

        # Verificar que se ingresó el número de documento
        if not numero_documento:
            return self.get(request, error="El número de documento es obligatorio.")

        # Verificar que la cantidad sea un número
        if not cantidad.isdigit():
            return self.get(request, error="La cantidad debe ser un número válido.")

        cantidad = int(cantidad)
        producto = Producto.objects.get(id=producto_id)

        # Actualizar stock
        producto.stock_actual += cantidad
        producto.save()

        # Crear movimiento de inventario
        MovimientoInventario.objects.create(
            producto=producto,
            cantidad=cantidad,
            tipo='entrada',
            usuario=request.user,
            numero_documento=numero_documento
        )

        return redirect('carga-manual')  # Redirigir después de guardar
