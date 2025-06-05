# rol/api/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # O tus permisos específicos

from rol.api.serializer import RolSerializer
from rol.application.use_cases import (
    ObtenerRolesUseCase,
    ObtenerRolPorIdUseCase,
    CrearRolUseCase,
    ActualizarRolUseCase,
    EliminarRolUseCase,
    RolNotFoundException,
    RolAlreadyExistsException
)
from rol.infrastructure.django_repositories import DjangoRolRepository

class RolViewSet(viewsets.ViewSet): # Cambiamos de ModelViewSet a ViewSet para mayor control
    serializer_class = RolSerializer
    permission_classes = [AllowAny] # Ajusta los permisos según tus necesidades

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rol_repo = DjangoRolRepository()
        self.obtener_roles_uc = ObtenerRolesUseCase(self.rol_repo)
        self.obtener_rol_por_id_uc = ObtenerRolPorIdUseCase(self.rol_repo)
        self.crear_rol_uc = CrearRolUseCase(self.rol_repo)
        self.actualizar_rol_uc = ActualizarRolUseCase(self.rol_repo)
        self.eliminar_rol_uc = EliminarRolUseCase(self.rol_repo)
        
    def list(self, request):
        roles_dominio = self.obtener_roles_uc.execute()
        serializer = self.serializer_class(roles_dominio, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            rol_dominio = self.obtener_rol_por_id_uc.execute(int(pk))
            serializer = self.serializer_class(rol_dominio)
            return Response(serializer.data)
        except RolNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        nombre = serializer.validated_data['nombre']
        permisos = serializer.validated_data.get('permisos', [])

        try:
            created_rol_domain = self.crear_rol_uc.execute(nombre=nombre, permisos=permisos)
            response_serializer = self.serializer_class(created_rol_domain)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except RolAlreadyExistsException as e:
            return Response({'nombre': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al crear rol: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        nombre = serializer.validated_data.get('nombre')
        permisos = serializer.validated_data.get('permisos')

        try:
            updated_rol_domain = self.actualizar_rol_uc.execute(rol_id=int(pk), nombre=nombre, permisos=permisos)
            response_serializer = self.serializer_class(updated_rol_domain)
            return Response(response_serializer.data)
        except RolNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except RolAlreadyExistsException as e:
            return Response({'nombre': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al actualizar rol: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            self.eliminar_rol_uc.execute(rol_id=int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RolNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al eliminar rol: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)