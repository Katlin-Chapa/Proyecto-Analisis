from django.views.generic import ListView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Factura, Venta, Stock
from .forms import FacturaForm, VentaFormset  # Asegúrate de importar tus formularios aquí

# Muestra la lista de todas las facturas
class FacturaView(ListView):
    model = Factura
    template_name = "facturas_lista.html"
    context_object_name = 'facturas'
    ordering = ['-fecha']
    paginate_by = 10


# Vista para generar una nueva factura y guardar los artículos vendidos
class VentaView(View):
    template_name = 'nueva_factura.html'

    def get(self, request):
        form = FacturaForm(request.GET or None)
        formset = VentaFormset(request.GET or None)  # Renderiza un formset vacío
        stocks = Stock.objects.filter(es_eliminado=False)  # Cambiado aquí
        context = {
            'form': form,
            'formset': formset,
            'stocks': stocks,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = FacturaForm(request.POST)
        formset = VentaFormset(request.POST)  # Recibe un método POST para el formset
        if form.is_valid() and formset.is_valid():
            # Guarda la factura
            factura_obj = form.save()
            for form in formset:  # Guarda cada formulario individual como su propio objeto
                venta_item = form.save(commit=False)
                venta_item.factura = factura_obj  # Asocia la factura con la venta
                stock = get_object_or_404(Stock, id=venta_item.stock.id)  # Obtiene el stock correspondiente
                venta_item.precio_unitario = stock.precio  # Asigna el precio del stock
                venta_item.precio_total = venta_item.cantidad * venta_item.precio_unitario  # Calcula el precio total

                # Actualiza la cantidad en la base de datos del stock
                stock.cantidad -= venta_item.cantidad
                stock.save()
                
                # Guarda el objeto de venta
                venta_item.save()

            messages.success(request, "La factura ha sido creada con éxito")
            return redirect('factura-detalle', numero=factura_obj.numero)  # Redirige a la vista de detalle de la factura
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
        
        context = {
            'form': form,
            'formset': formset,
            'stocks': Stock.objects.filter(is_deleted=False),  # Vuelve a obtener stocks para mostrar
        }
        return render(request, self.template_name, context)
