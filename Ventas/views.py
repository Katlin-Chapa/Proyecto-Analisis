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
            'stocks': Stock.objects.filter(es_eliminado=False),  # Vuelve a obtener stocks para mostrar
        }
        return render(request, self.template_name, context)

from django.http import JsonResponse
from .models import Stock

def get_stock_price(request, stock_id):
    try:
        stock = Stock.objects.get(id=stock_id)
        return JsonResponse({'precio': stock.precio})
    except Stock.DoesNotExist:
        return JsonResponse({'error': 'Stock no encontrado'}, status=404)

# views.py
from django.views import View
from django.http import JsonResponse
from .models import Factura, Venta

class GuardarVentaView(View):
    def post(self, request):
        print(request.POST)  # Para depuración

        # Crear la factura
        factura = Factura(
            nombre=request.POST.get('nombre'),
            telefono=request.POST.get('telefono'),
            correo_electronico=request.POST.get('correo_electronico'),
            direccion=request.POST.get('direccion'),
            nit=request.POST.get('nit')
        )
        factura.save()  # Guardamos la factura

        # Obtener total_items con un valor por defecto de 0
        total_items = request.POST.get('total_items', '0')

        # Asegurarse de que sea un entero antes de usarlo
        try:
            total_items = int(total_items)
        except ValueError:
            return JsonResponse({'success': False, 'error': 'total_items inválido'})

        # Crear las ventas asociadas
        for i in range(total_items):
            stock_id = request.POST.get(f'stock_{i}')
            cantidad = request.POST.get(f'cantidad_{i}')

            if stock_id and cantidad:
                try:
                    cantidad = int(cantidad)
                    stock = Stock.objects.get(id=stock_id)  # Asegúrate de que el stock existe

                    # Crear la venta con el precio unitario obtenido del stock
                    venta = Venta(
                        factura=factura,
                        stock=stock,
                        cantidad=cantidad,
                        precio_unitario=stock.precio  # Asignar el precio unitario aquí
                    )
                    venta.save()  # Guardar la venta
                except (Stock.DoesNotExist, ValueError):
                    return JsonResponse({'success': False, 'error': 'stock o cantidad inválido'})

        return JsonResponse({'success': True})
