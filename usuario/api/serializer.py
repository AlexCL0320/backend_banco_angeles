# usuario/api/serializer.py (Revisión)

from rest_framework import serializers
from usuario.models import Usuario
import re

from usuario.domain.entities import Usuario as DomainUsuario, Rol as DomainRol

class UsuarioSerializer(serializers.ModelSerializer):
    rol_id = serializers.IntegerField(write_only=True, required=False, allow_null=True) # Acepta rol_id como opcional
    rol_nombre = serializers.CharField(source='rol.nombre', read_only=True)

    # ... (Tus validaciones personalizadas se mantienen)

    class Meta:
        model = Usuario
        fields = ['id', 'nombre_usuario', 'correo', 'sexo', 'password', 'rol_id', 'rol_nombre', 'is_active', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False, 'allow_null': True}, # 'required=False' y 'allow_null=True' para update
            'rol_id': {'required': False, 'allow_null': True} # Hacer rol_id opcional para el serializer
        }
    
    def to_representation(self, instance):
        if isinstance(instance, DomainUsuario):
            data = {
                'id': instance.id,
                'nombre_usuario': instance.nombre_usuario,
                'correo': instance.correo,
                'sexo': instance.sexo,
                'rol_id': instance.rol.id if instance.rol else None, # Asegurarse de manejar el caso donde el rol podría ser None
                'rol_nombre': instance.rol.nombre if instance.rol else None,
                'is_active': instance.is_active,
                'is_staff': instance.is_staff,
            }
            return data
        elif isinstance(instance, Usuario):
            return super().to_representation(instance)
        return {}