# municipio/api/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny # Mantén IsAuthenticated si es necesario

from municipio.api.serializer import MunicipioSerializer
from municipio.application.use_cases import (
    ObtenerMunicipiosUseCase,
    ObtenerMunicipioPorIdUseCase,
    CrearMunicipioUseCase,
    ActualizarMunicipioUseCase,
    EliminarMunicipioUseCase,
    MunicipioNotFoundException,
    MunicipioAlreadyExistsException
)
from municipio.infrastructure.django_repositories import DjangoMunicipioRepository

class MunicipioViewSet(viewsets.ViewSet): # Cambiamos de ModelViewSet a ViewSet
    serializer_class = MunicipioSerializer
    permission_classes = [IsAuthenticated] # Ajusta tus permisos según necesites

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.municipio_repo = DjangoMunicipioRepository()
        self.obtener_municipios_uc = ObtenerMunicipiosUseCase(self.municipio_repo)
        self.obtener_municipio_por_id_uc = ObtenerMunicipioPorIdUseCase(self.municipio_repo)
        self.crear_municipio_uc = CrearMunicipioUseCase(self.municipio_repo)
        self.actualizar_municipio_uc = ActualizarMunicipioUseCase(self.municipio_repo)
        self.eliminar_municipio_uc = EliminarMunicipioUseCase(self.municipio_repo)
        
    def list(self, request):
        municipios_dominio = self.obtener_municipios_uc.execute()
        serializer = self.serializer_class(municipios_dominio, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            municipio_dominio = self.obtener_municipio_por_id_uc.execute(int(pk))
            serializer = self.serializer_class(municipio_dominio)
            return Response(serializer.data)
        except MunicipioNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        nombre = serializer.validated_data['nombre']

        try:
            created_municipio_domain = self.crear_municipio_uc.execute(nombre=nombre)
            response_serializer = self.serializer_class(created_municipio_domain)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except MunicipioAlreadyExistsException as e:
            return Response({'nombre': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al crear municipio: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        nombre = serializer.validated_data.get('nombre')

        try:
            updated_municipio_domain = self.actualizar_municipio_uc.execute(municipio=int(pk), nombre=nombre)
            response_serializer = self.serializer_class(updated_municipio_domain)
            return Response(response_serializer.data)
        except MunicipioNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except MunicipioAlreadyExistsException as e:
            return Response({'nombre': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al actualizar municipio: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            self.eliminar_municipio_uc.execute(municipio=int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except MunicipioNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al eliminar municipio: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)