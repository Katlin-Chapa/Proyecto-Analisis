from django.contrib import admin
from .models import Factura, Venta

# Configuración del modelo Factura para el admin
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'nombre', 'telefono', 'correo_electronico', 'nit', 'direccion', 'fecha')  # Añadí 'tiempo'
    search_fields = ('numero', 'nombre')  # Añadir barra de búsqueda por número de factura y nombre
    list_filter = ('fecha',)  # Filtrar por fecha (tiempo)

# Configuración del modelo Venta para el admin
class VentaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'stock', 'cantidad', 'precio_unitario', 'precio_total')  # Campos a mostrar
    search_fields = ('factura__numero',)  # Añadir búsqueda por número de factura y nombre del stock
    list_filter = ('factura__fecha',)  # Filtrar por fecha de factura y por stock

# Registrar los modelos en el admin
admin.site.register(Factura, FacturaAdmin)
admin.site.register(Venta, VentaAdmin)
