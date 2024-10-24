from django.db import models
from django.contrib.auth.models import User  # Importa el modelo User
from Inventario.models import Stock

class Factura(models.Model):
    numero = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=150)
    telefono = models.IntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo_electronico = models.EmailField(max_length=254, blank=True, null=True)
    nit = models.IntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Registro del usuario que creó la factura

    def __str__(self):
        return f"No. factura: {self.numero}"

    def obtener_lista_de_articulos(self):
        return ArticuloVenta.objects.filter(factura=self)

    def obtener_precio_total(self):
        articulos_de_venta = ArticuloVenta.objects.filter(factura=self)
        total = 0
        for articulo in articulos_de_venta:
            total += articulo.precio_total
        return total

class ArticuloVenta(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='articulos')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.cantidad} unidades de {self.stock.nombre} vendidos"

    def save(self, *args, **kwargs):
        # Aquí se asegura de que el precio unitario provenga del modelo Stock
        self.precio_unitario = self.stock.precio
        self.precio_total = self.cantidad * self.precio_unitario  # Calcula el precio total
        super().save(*args, **kwargs)
