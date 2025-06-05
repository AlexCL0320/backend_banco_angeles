# usuario/api/views.py

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from usuario.api.permissions import IsOwnerOrAdmin
from usuario.api.serializer import UsuarioSerializer

# Importar TU MODELO de Django aquí
from usuario.models import Usuario as DjangoUsuario # <--- ¡IMPORTA TU MODELO DE DJANGO!

# Importar casos de uso y excepciones
from usuario.application.use_cases import (
    ObtenerUsuariosUseCase,
    ObtenerUsuarioPorIdUseCase,
    CrearUsuarioUseCase,
    ActualizarUsuarioUseCase,
    EliminarUsuarioUseCase,
    UsuarioNotFoundException,
    EmailAlreadyExistsException,
    RolNotFoundException
)
# Importar implementaciones de repositorios
from usuario.infrastructure.django_repositories import DjangoUsuarioRepository, DjangoRolRepository

class UsuarioViewSet(viewsets.ModelViewSet):
    # Ya importamos DjangoUsuario arriba
    queryset = DjangoUsuario.objects.all() # <--- Ahora 'DjangoUsuario' está definido
    serializer_class = UsuarioSerializer # <--- ¡AÑADE ESTA LÍNEA!
    permission_classes = [AllowAny]

    def get_permissions(self):
        # ... (Tus permisos se mantienen)
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'list':
            return [AllowAny()]
        elif self.action == 'retrieve':
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rol_repo = DjangoRolRepository()
        self.user_repo = DjangoUsuarioRepository(self.rol_repo)
        
        self.obtener_usuarios_uc = ObtenerUsuariosUseCase(self.user_repo)
        self.obtener_usuario_por_id_uc = ObtenerUsuarioPorIdUseCase(self.user_repo)
        self.crear_usuario_uc = CrearUsuarioUseCase(self.user_repo, self.rol_repo)
        self.actualizar_usuario_uc = ActualizarUsuarioUseCase(self.user_repo, self.rol_repo)
        self.eliminar_usuario_uc = EliminarUsuarioUseCase(self.user_repo)

    def list(self, request, *args, **kwargs):
        usuarios_dominio = self.obtener_usuarios_uc.execute()
        serializer = self.get_serializer(usuarios_dominio, many=True) # Usa self.get_serializer
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            django_user_obj = self.get_object() 
            usuario_dominio = self.obtener_usuario_por_id_uc.execute(user_id=django_user_obj.id)
            serializer = self.get_serializer(usuario_dominio) # Usa self.get_serializer
            return Response(serializer.data)
        except UsuarioNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Error interno del servidor', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # Usa self.get_serializer
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        try:
            rol_id_from_request = data.get('rol_id')
            password_from_request = data.get('password') # Obtener la contraseña del serializer
            
            created_user_domain = self.crear_usuario_uc.execute(
                nombre_usuario=data['nombre_usuario'],
                correo=data['correo'],
                sexo=data['sexo'],
                password=password_from_request, # Pasa la contraseña al caso de uso
                rol_id=rol_id_from_request 
            )
            response_serializer = self.get_serializer(created_user_domain) # Usa self.get_serializer
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except EmailAlreadyExistsException as e:
            return Response({'correo': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except RolNotFoundException as e:
            return Response({'rol_id': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'Error interno del servidor al crear usuario', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None, *args, **kwargs):
        django_user_obj = self.get_object() 

        serializer = self.get_serializer(data=request.data, partial=True) # Usa self.get_serializer
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        
        update_data_for_uc = {
            'nombre_usuario': data.get('nombre_usuario'),
            'correo': data.get('correo'),
            'sexo': data.get('sexo'),
            'password': data.get('password'), 
            'is_active': data.get('is_active'),
            'is_staff': data.get('is_staff'),
        }
        if 'rol_id' in data:
            update_data_for_uc['rol_id'] = data['rol_id']

        update_data_for_uc = {k: v for k, v in update_data_for_uc.items() if v is not None}
        
        try:
            updated_user_domain = self.actualizar_usuario_uc.execute(
                user_id=django_user_obj.id,
                update_data=update_data_for_uc
            )
            response_serializer = self.get_serializer(updated_user_domain) # Usa self.get_serializer
            return Response(response_serializer.data)
        except UsuarioNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except EmailAlreadyExistsException as e:
            return Response({'correo': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except RolNotFoundException as e:
            return Response({'rol_id': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'Error interno del servidor al actualizar usuario', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def destroy(self, request, pk=None, *args, **kwargs):
        django_user_obj = self.get_object() 
        
        try:
            self.eliminar_usuario_uc.execute(user_id=django_user_obj.id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UsuarioNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Error interno del servidor al eliminar usuario', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Para el usuario logeado
class UsuarioAutenticadoView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rol_repo = DjangoRolRepository()
        self.user_repo = DjangoUsuarioRepository(self.rol_repo)
        self.obtener_usuario_por_id_uc = ObtenerUsuarioPorIdUseCase(self.user_repo)

    def get(self, request):
        user_id = request.user.id
        try:
            user_domain = self.obtener_usuario_por_id_uc.execute(user_id)
            serializer = UsuarioSerializer(user_domain)
            return Response(serializer.data)
        except UsuarioNotFoundException as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Error al obtener datos del usuario autenticado', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)