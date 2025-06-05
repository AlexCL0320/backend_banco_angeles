# coordenada/api/serializer.py

from rest_framework import serializers

# Clase serializador para la entidad de dominio Coordenada
class CoordenadaSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    latitud = serializers.CharField(max_length=100, required=True) # Modificado a CharField
    longitud = serializers.CharField(max_length=100, required=True) # Modificado a CharField

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass