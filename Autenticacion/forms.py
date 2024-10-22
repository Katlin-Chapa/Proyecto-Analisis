from django import forms

class InicioFormulario(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Nombre de usuario',
        'id': 'username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
        'id': 'password'
    }))

class SupportForm(forms.Form):
    subject = forms.CharField(max_length=100, label='Asunto')
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')