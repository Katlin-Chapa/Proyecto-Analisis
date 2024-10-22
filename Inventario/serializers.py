from rest_framework import serializers
from .models import Producto, MovimientoInventario

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class MovimientoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimientoInventario
        fields = '__all__'
        read_only_fields = ['fecha', 'usuario']

    def validate(self, data):
        if 'numero_documento' not in data or not data['numero_documento']:
            raise serializers.ValidationError("El número de documento es obligatorio.")
        return data
