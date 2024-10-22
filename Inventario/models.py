from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Asegúrate de que este campo esté presente
    fecha_carga = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
