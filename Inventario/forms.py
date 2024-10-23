from django import forms
from .models import Stock, Categoria

class CategoriaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer clases CSS para el campo
        self.fields['nombre'].widget.attrs.update({'class': 'textinput form-control'})

    class Meta:
        model = Categoria
        fields = ['nombre']  # Solo necesitas el campo 'nombre'
        
class StockForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer clases CSS para los campos
        self.fields['nombre'].widget.attrs.update({'class': 'textinput form-control'})  # Campo nombre
        self.fields['cantidad'].widget.attrs.update({'class': 'textinput form-control', 'min': '0'})  # Campo cantidad
        self.fields['categoria'].widget.attrs.update({'class': 'form-control'})  # Campo categoría
        self.fields['fecha_vencimiento'].widget.attrs.update({'class': 'textinput form-control', 'type': 'date'})  # Campo fecha vencimiento
        self.fields['numero_documento'].widget.attrs.update({'class': 'textinput form-control'})  # Campo número de documento
        self.fields['dosis'].widget.attrs.update({'class': 'textinput form-control'})  # Campo dosis
        self.fields['imagen'].widget.attrs.update({'class': 'form-control'})  # Campo imagen

    class Meta:
        model = Stock
        fields = ['nombre', 'cantidad', 'fecha_vencimiento', 'numero_documento', 'dosis', 'imagen', 'categoria']  # Incluye todos los campos relevantes
