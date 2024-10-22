from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio', 'stock_actual', 'stock_minimo', 'fecha_caducidad', 'imagen']  # Asegúrate de que todos los campos necesarios estén aquí

from .models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']