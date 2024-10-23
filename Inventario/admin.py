from django.contrib import admin
from .models import Stock, Categoria

class StockAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'fecha_vencimiento', 'categoria', 'numero_documento')
    list_editable = ('cantidad', 'numero_documento')
    search_fields = ('nombre',)
    list_filter = ('categoria',)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

admin.site.register(Stock, StockAdmin)
admin.site.register(Categoria, CategoriaAdmin)
