from django.db import models
from django.conf import settings

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_caducidad = models.DateField()
    dosis = models.CharField(max_length=50)
    stock_actual = models.PositiveIntegerField()
    stock_minimo = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  

    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}"

class MovimientoInventario(models.Model):
    TIPOS_MOVIMIENTO = (
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    )
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    tipo = models.CharField(choices=TIPOS_MOVIMIENTO, max_length=10)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numero_documento = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.tipo} de {self.cantidad} de {self.producto.nombre}"
