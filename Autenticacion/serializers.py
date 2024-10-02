from rest_framework import serializers

class InicioSerializador(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
