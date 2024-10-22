from django.contrib import admin
from .models import Categoria, Producto, MovimientoInventario

# Registro del modelo Categoria
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  
    search_fields = ('nombre',)  

# Registro del modelo Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'stock_actual', 'stock_minimo', 'fecha_caducidad')  
    list_filter = ('categoria',)  
    search_fields = ('nombre', 'categoria__nombre')  

# Registro del modelo MovimientoInventario
@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'producto', 'cantidad', 'tipo', 'fecha', 'usuario')  
    list_filter = ('tipo', 'fecha', 'usuario')  
    search_fields = ('producto__nombre', 'usuario__username')  
