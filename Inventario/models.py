from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)  # Nombre del medicamento
    cantidad = models.IntegerField(default=1)  # Cantidad disponible
    fecha_vencimiento = models.DateField()  # Fecha de vencimiento
    fecha_ingreso = models.DateField(auto_now_add=True)  # Fecha de ingreso al inventario
    numero_documento = models.CharField(max_length=50, blank=True, null=True)  # Número del documento relacionado
    dosis = models.CharField(max_length=50)  # Dosis del medicamento (ej: 10 mg, 1 L)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)  # Imagen del medicamento
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)  # Categoría del medicamento
    es_eliminado = models.BooleanField(default=False)  # Marca para eliminación lógica

    def __str__(self):
        return self.nombre
