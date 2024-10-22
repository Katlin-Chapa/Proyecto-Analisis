from django.contrib import admin
from .models import Producto
from django.utils.safestring import mark_safe

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'fecha_carga', 'imagen')  # Campos a mostrar en la lista
    search_fields = ('nombre',)  # Permitir búsqueda por nombre
    list_filter = ('fecha_carga',)  # Filtros por fecha de carga

    # Para permitir la carga de imágenes en el formulario de administración
    def imagen_preview(self, obj):
        if obj.imagen:
            return mark_safe(f'<img src="{obj.imagen.url}" width="50" height="50" />')
        return "-"
    imagen_preview.short_description = 'Imagen'

    # Puedes agregar más configuraciones aquí si lo deseas

admin.site.register(Producto, ProductoAdmin)
