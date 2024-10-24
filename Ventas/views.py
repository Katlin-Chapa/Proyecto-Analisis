from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Factura, ArticuloVenta, Stock
from .forms import FacturaForm, ArticuloVentaFormset, SeleccionarClienteForm

# Muestra la lista de facturas de todas las ventas
class FacturaView(ListView):
    model = Factura
    template_name = "lista_facturas.html"
    context_object_name = 'facturas'
    ordering = ['-fecha']
    paginate_by = 10

# Usado para generar una factura y guardar los artículos
class CrearFacturaView(View):                                                      
    template_name = 'nueva_factura.html'

    def get(self, request):
        form = FacturaForm(request.GET or None)
        formset = ArticuloVentaFormset(request.GET or None)                         
        stocks = Stock.objects.filter(es_eliminado=False)
        context = {
            'form'      : form,
            'formset'   : formset,
            'stocks'    : stocks
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = FacturaForm(request.POST)
        formset = ArticuloVentaFormset(request.POST)                                 
        if form.is_valid() and formset.is_valid():
            # Guardar factura
            factura_obj = form.save(commit=False)
            factura_obj.usuario = request.user  # Asignar usuario autenticado
            factura_obj.save()     
            
            for form in formset:                                                    
                articulo = form.save(commit=False)
                articulo.factura = factura_obj                                       
                # Obtener stock relacionado
                stock = get_object_or_404(Stock, nombre=articulo.stock.nombre)      
                # Calcular precio total
                articulo.precio_total = articulo.precio_unitario * articulo.cantidad
                # Actualizar cantidad en stock
                stock.cantidad -= articulo.cantidad   
                # Guardar artículo de la venta y actualizar stock
                stock.save()
                articulo.save()

            messages.success(request, "Los artículos han sido registrados correctamente")
            return redirect('factura-detalle', numero=factura_obj.numero)

        context = {
            'form'      : form,
            'formset'   : formset,
        }
        return render(request, self.template_name, context)

# Muestra los detalles de una factura
class FacturaDetalleView(View):
    model = Factura
    template_name = "factura_detalle.html"
    factura_base = "factura_base.html"
    
    def get(self, request, numero):
        context = {
            'factura'        : Factura.objects.get(numero=numero),
            'articulos'      : ArticuloVenta.objects.filter(factura=numero),
            'factura_base'   : self.factura_base,
        }
        return render(request, self.template_name, context)