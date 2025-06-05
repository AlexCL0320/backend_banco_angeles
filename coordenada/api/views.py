# coordenada/api/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # Considera añadir permisos aquí

from coordenada.api.serializer import CoordenadaSerializer
from coordenada.application.use_cases import (
    ObtenerCoordenadasUseCase,
    ObtenerCoordenadaPorIdUseCase,
    CrearCoordenadaUseCase,
    ActualizarCoordenadaUseCase,
    EliminarCoordenadaUseCase,
    CoordenadaNotFoundException,
    CoordenadaAlreadyExistsException
)
from coordenada.infrastructure.django_repositories import DjangoCoordenadaRepository

class CoordenadaViewSet(viewsets.ViewSet):
    serializer_class = CoordenadaSerializer
    permission_classes = [AllowAny] # Ajusta tus permisos (ej. [IsAuthenticated])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.coordenada_repo = DjangoCoordenadaRepository()
        self.obtener_coordenadas_uc = ObtenerCoordenadasUseCase(self.coordenada_repo)
        self.obtener_coordenada_por_id_uc = ObtenerCoordenadaPorIdUseCase(self.coordenada_repo)
        self.crear_coordenada_uc = CrearCoordenadaUseCase(self.coordenada_repo)
        self.actualizar_coordenada_uc = ActualizarCoordenadaUseCase(self.coordenada_repo)
        self.eliminar_coordenada_uc = EliminarCoordenadaUseCase(self.coordenada_repo)
        
    def list(self, request):
        coordenadas_dominio = self.obtener_coordenadas_uc.execute()
        serializer = self.serializer_class(coordenadas_dominio, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            coordenada_dominio = self.obtener_coordenada_por_id_uc.execute(int(pk))
            serializer = self.serializer_class(coordenada_dominio)
            return Response(serializer.data)
        except CoordenadaNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        latitud = serializer.validated_data['latitud']
        longitud = serializer.validated_data['longitud']

        try:
            created_coordenada_domain = self.crear_coordenada_uc.execute(latitud=latitud, longitud=longitud)
            response_serializer = self.serializer_class(created_coordenada_domain)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except CoordenadaAlreadyExistsException as e:
            return Response({'latitud/longitud': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al crear coordenada: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        latitud = serializer.validated_data.get('latitud')
        longitud = serializer.validated_data.get('longitud')

        try:
            updated_coordenada_domain = self.actualizar_coordenada_uc.execute(
                coordenada_id=int(pk),
                latitud=latitud,
                longitud=longitud
            )
            response_serializer = self.serializer_class(updated_coordenada_domain)
            return Response(response_serializer.data)
        except CoordenadaNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except CoordenadaAlreadyExistsException as e:
            return Response({'latitud/longitud': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al actualizar coordenada: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk=None):
        try:
            self.eliminar_coordenada_uc.execute(coordenada_id=int(pk))
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CoordenadaNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'Error interno del servidor al eliminar coordenada: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)