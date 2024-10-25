from django import forms
from .models import Factura, Venta, Stock  # Asegúrate de importar tus modelos aquí

# Formulario para la factura
class FacturaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '150', 'required': 'true'})
        self.fields['telefono'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '10', 'pattern': '[0-9]{10}', 'title': 'Números solamente'})
        self.fields['direccion'].widget.attrs.update({'class': 'textinput form-control', 'maxlength': '200'})
        self.fields['correo_electronico'].widget.attrs.update({'class': 'textinput form-control'})
        self.fields['nit'].widget.attrs.update({'class': 'textinput form-control', 'pattern': '[0-9]+', 'title': 'Números solamente'})

    class Meta:
        model = Factura
        fields = ['nombre', 'telefono', 'direccion', 'correo_electronico', 'nit']
        widgets = {
            'direccion': forms.Textarea(
                attrs={
                    'class': 'textinput form-control',
                    'rows': '2'
                }
            )
        }

# Formulario para la venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['factura', 'stock', 'cantidad', 'precio_unitario', 'precio_total']
        widgets = {
            'precio_unitario': forms.TextInput(attrs={'class': 'textinput form-control', 'readonly': 'true'}),
            'precio_total': forms.TextInput(attrs={'class': 'textinput form-control', 'readonly': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['factura'].widget.attrs.update({'class': 'textinput form-control', 'required': 'true'})
        self.fields['stock'].queryset = Stock.objects.filter(es_eliminado=False)
        self.fields['stock'].widget.attrs.update({'class': 'textinput form-control stock', 'required': 'true'})
        self.fields['cantidad'].widget.attrs.update({'class': 'textinput form-control', 'min': '1', 'required': 'true'})

        # Escuchamos los cambios en el stock para asignar el precio unitario automáticamente
        if 'stock' in self.data:
            try:
                stock_id = int(self.data.get('stock'))
                self.fields['precio_unitario'].initial = Stock.objects.get(id=stock_id).precio
            except (ValueError, Stock.DoesNotExist):
                pass
        elif self.instance.pk:
            self.fields['precio_unitario'].initial = self.instance.stock.precio

    def clean(self):
        cleaned_data = super().clean()
        cantidad = cleaned_data.get('cantidad')
        precio_unitario = cleaned_data.get('precio_unitario')

        # Calcular el precio total basado en la cantidad y el precio unitario
        if cantidad and precio_unitario is not None:
            cleaned_data['precio_total'] = cantidad * precio_unitario

        return cleaned_data

# Formset utilizado para renderizar múltiples 'VentaForm'
from django.forms import formset_factory
VentaFormset = formset_factory(VentaForm, extra=1)
