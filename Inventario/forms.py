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

from django import forms
from .models import Lote, Stock

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['stock', 'cantidad', 'numero_documento', 'fecha_vencimiento']

from django import forms
from .models import Stock, Lote

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['nombre', 'cantidad', 'precio', 'dosis', 'imagen', 'categoria', 'numero_documento']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del medicamento'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad disponible'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Precio del medicamento'
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dosis del medicamento'
            }),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-control'
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de documento relacionado'
            })
        }
        labels = {
            'nombre': 'Nombre del Medicamento',
            'cantidad': 'Cantidad',
            'precio': 'Precio',
            'dosis': 'Dosis',
            'imagen': 'Imagen',
            'categoria': 'Categoría',
            'numero_documento': 'Número de Documento'
        }


