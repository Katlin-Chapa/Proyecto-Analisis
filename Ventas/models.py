from django.db import models
from Inventario.models import Stock

# Contiene las facturas de ventas realizadas
class Factura(models.Model):
    numero = models.AutoField(primary_key=True)
    fecha = models.DateField(auto_now_add=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.IntegerField(blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo_electronico = models.EmailField(max_length=254, blank=True, null=True)
    nit = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Factura no: " + str(self.numero)

    def obtener_lista_items(self):
        return Venta.objects.filter(factura=self)

    def obtener_precio_total(self):
        items_venta = Venta.objects.filter(factura=self)
        total = 0
        for item in items_venta:
            total += item.precio_total
        return total

# Contiene los artículos vendidos
class Venta(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='factura_items')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='item_venta')
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # El precio se tomará del Stock
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return "Factura no: " + str(self.factura.numero) + ", Artículo = " + self.stock.nombre

    def save(self, *args, **kwargs):
        # Asignar el precio unitario directamente desde el modelo Stock
        self.precio_unitario = self.stock.precio
        # Calcular el precio total basado en la cantidad
        self.precio_total = self.cantidad * self.precio_unitario
        super(Venta, self).save(*args, **kwargs)