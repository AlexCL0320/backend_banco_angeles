# municipio/api/serializer.py

from rest_framework import serializers
# Ya no importamos municipio.models.Municipio aquí directamente para la serialización de la API,
# sino que trabajamos con la entidad de dominio.

# Clase serializador para la entidad de dominio Municipio
class MunicipioSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        # Este método no será llamado directamente por las vistas en una Clean Architecture
        # Los casos de uso manejarán la creación. Este serializador es para entrada/salida.
        pass 

    def update(self, instance, validated_data):
        # Este método no será llamado directamente por las vistas en una Clean Architecture
        # Los casos de uso manejarán la actualización.
        pass