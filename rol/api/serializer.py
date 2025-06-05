# rol/api/serializer.py

from rest_framework import serializers
# Ya no importamos rol.models.Rol aquí directamente para la serialización de la API,
# sino que trabajamos con la entidad de dominio.

# Clase serializador para la entidad de dominio Rol
class RolSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=50, required=True)
    permisos = serializers.ListField(child=serializers.CharField(), required=False, default=list)

    def create(self, validated_data):
        # Este método no será llamado directamente por las vistas en una Clean Architecture
        # Los casos de uso manejarán la creación. Este serializador es para entrada/salida.
        pass 

    def update(self, instance, validated_data):
        # Este método no será llamado directamente por las vistas en una Clean Architecture
        # Los casos de uso manejarán la actualización.
        pass