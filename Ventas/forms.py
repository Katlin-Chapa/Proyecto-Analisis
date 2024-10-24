from django import forms
from django.forms import formset_factory
from .models import Factura, ArticuloVenta
from Inventario.models import Stock

# Formulario utilizado para seleccionar un cliente
class SeleccionarClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'textinput form-control', 'pattern' : '[a-zA-Z\s]{1,50}', 'title' : 'Solo letras y espacios', 'required': 'true'})
        self.fields['telefono'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern' : '[0-9]{10}', 'title' : 'Solo números', 'required': 'true'})
        self.fields['correo_electronico'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['nit'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '15', 'pattern' : '[0-9]{10}', 'title' : 'Solo números', 'required': 'true'})
    class Meta:
        model = Factura
        fields = ['nombre', 'telefono', 'direccion', 'correo_electronico', 'nit']
        widgets = {
            'direccion': forms.Textarea(
                attrs = {
                    'class': 'textinput form-control',
                    'rows': '2'
                }
            )
        }

# Formulario utilizado para representar un solo artículo en una venta
class ArticuloVentaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].queryset = Stock.objects.filter(es_eliminado=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control setprice stock', 'required': 'true'})
        self.fields['cantidad'].widget.attrs.update({'class': 'textinput form-control setprice cantidad', 'min': '0', 'required': 'true'})
        self.fields['precio_unitario'].widget.attrs.update({'class': 'textinput form-control setprice precio', 'min': '0', 'required': 'true'})
    class Meta:
        model = ArticuloVenta
        fields = ['stock', 'cantidad', 'precio_unitario']

# Formset utilizado para representar múltiples formularios de 'ArticuloVentaForm'
ArticuloVentaFormset = formset_factory(ArticuloVentaForm, extra=1)

# Formulario utilizado para aceptar otros detalles de la factura
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['direccion', 'correo_electronico', 'telefono', 'nit']
