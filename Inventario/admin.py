from django.contrib import admin
from .models import Categoria, Producto, MovimientoInventario

# Registro del modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Muestra el id y el nombre en la lista
    search_fields = ('nombre',)  # Campo que se puede buscar

# Registro del modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock_actual', 'stock_minimo', 'fecha_caducidad')  # Campos a mostrar
    list_filter = ('categoria',)  # Filtros por categoría
    search_fields = ('nombre', 'categoria__nombre')  # Campos que se pueden buscar

# Registro del modelo MovimientoInventario
@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'tipo', 'fecha', 'usuario')  # Campos a mostrar
    list_filter = ('tipo', 'fecha', 'usuario')  # Filtros por tipo, fecha y usuario
    search_fields = ('producto__nombre', 'usuario__username')  # Campos que se pueden buscar
