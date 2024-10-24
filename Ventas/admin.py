from django.contrib import admin
from .models import Factura, ArticuloVenta

# Registro de los modelos en el admin
admin.site.register(Factura)
admin.site.register(ArticuloVenta)
