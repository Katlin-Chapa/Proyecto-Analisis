from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Stock, Lote, Categoria
from .forms import StockForm, LoteForm
from django_filters.views import FilterView
from .filters import StockFilter
from reportlab.pdfgen import canvas
from openpyxl import Workbook

class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(es_eliminado=False)
    template_name = 'inventario.html'


class CargarProductosAnualmente(ListView):
    model = Stock
    template_name = 'cargar_productos.html'
    context_object_name = 'productos'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Stock.objects.filter(nombre__icontains=query, es_eliminado=False)
        return Stock.objects.filter(es_eliminado=False)


def crear_lote(request):
    if request.method == 'POST':
        form = LoteForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            stock_id = request.POST.get('stock')
            lote.stock = get_object_or_404(Stock, id=stock_id)
            stock = lote.stock
            stock.cantidad += lote.cantidad
            stock.save()
            lote.save()
            return redirect('cargar-productos')
    else:
        form = LoteForm()
    
    return render(request, 'crear_lote.html', {'form': form})


def obtener_lotes(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    lotes = stock.lotes.all()
    data = [{'numero_documento': lote.numero_documento, 'fecha_vencimiento': lote.fecha_vencimiento} for lote in lotes]
    return JsonResponse({'lotes': data})


def agregar_categoria_producto(request):
    if request.method == 'POST':
        if 'nombre_categoria' in request.POST:
            nombre_categoria = request.POST.get('nombre_categoria')
            Categoria.objects.create(nombre=nombre_categoria)
            return redirect('agregar')
        elif 'nombre_producto' in request.POST:
            nombre_producto = request.POST.get('nombre_producto')
            cantidad = request.POST.get('cantidad')
            precio = request.POST.get('precio')
            dosis = request.POST.get('dosis')
            numero_documento = request.POST.get('numero_documento')
            fecha_vencimiento = request.POST.get('fecha_vencimiento')
            categoria = get_object_or_404(Categoria, id=request.POST.get('categoria'))
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
            return redirect('agregar')

    categorias = Categoria.objects.all()
    return render(request, 'agregar.html', {'categorias': categorias})


def modificar_producto(request, id):
    stock = get_object_or_404(Stock, id=id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        stock.nombre = request.POST.get('nombre')
        stock.cantidad = request.POST.get('cantidad')
        stock.precio = request.POST.get('precio')
        stock.dosis = request.POST.get('dosis')
        stock.categoria_id = request.POST.get('categoria')
        imagen = request.FILES.get('imagen')

        if imagen:
            stock.imagen = imagen

        stock.save()
        return redirect('inventario')

    context = {
        'stock': stock,
        'categorias': categorias,
    }
    return render(request, 'modificar.html', context)


@login_required
def eliminar_producto(request, stock_id):
    producto = get_object_or_404(Stock, id=stock_id)
    producto.delete()
    return redirect(reverse('inventario'))


def generar_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="stock.pdf"'
    p = canvas.Canvas(response)

    p.drawString(100, 800, "Listado de Stock")
    y = 750
    for stock in Stock.objects.all():
        p.drawString(100, y, f"Nombre: {stock.nombre}, Cantidad: {stock.cantidad}, Precio: {stock.precio}")
        y -= 20

    p.showPage()
    p.save()
    return response


def generar_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stock"
    ws.append(['Nombre', 'Cantidad', 'Precio', 'Fecha de Vencimiento'])

    for stock in Stock.objects.all():
        ws.append([stock.nombre, stock.cantidad, stock.precio, stock.fecha_vencimiento])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="stock.xlsx"'
    wb.save(response)
    return response


def generar_lote_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lote.pdf"'
    p = canvas.Canvas(response)

    p.drawString(100, 800, "Listado de Lotes")
    y = 750
    for lote in Lote.objects.all():
        p.drawString(100, y, f"Stock: {lote.stock.nombre}, Cantidad: {lote.cantidad}, Documento: {lote.numero_documento}, Fecha Vencimiento: {lote.fecha_vencimiento}")
        y -= 20

    p.showPage()
    p.save()
    return response


def generar_lote_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Lotes"
    ws.append(['Stock', 'Cantidad', 'Documento', 'Fecha de Vencimiento'])

    for lote in Lote.objects.all():
        ws.append([lote.stock.nombre, lote.cantidad, lote.numero_documento, lote.fecha_vencimiento])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="lotes.xlsx"'
    wb.save(response)
    return response

def reportes_view(request):
    # Obtener todos los stock que no están eliminados
    stocks = Stock.objects.filter(es_eliminado=False)
    # Obtener todos los lotes
    lotes = Lote.objects.all()
    # Renderizar la plantilla y pasar los datos
    return render(request, 'reportes.html', {'stocks': stocks, 'lotes': lotes})

