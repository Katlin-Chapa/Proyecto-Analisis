from django.contrib import admin
from .models import Stock, Categoria

class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'cantidad', 'precio', 'fecha_vencimiento', 'fecha_ingreso', 'numero_documento', 'dosis', 'imagen', 'categoria', 'es_eliminado')
    list_editable = ('cantidad', 'numero_documento', 'precio', 'es_eliminado')
    search_fields = ('nombre',)
    list_filter = ('categoria',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Stock, StockAdmin)
admin.site.register(Categoria, CategoriaAdmin)
