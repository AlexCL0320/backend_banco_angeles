"""
URL configuration for bancoSangre project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse

from donador.api.views_mapa import donadores_para_mapa
from usuario.api.views import UsuarioViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Ruta raíz para evitar error 404 en /
def home(request):
    return HttpResponse("Bienvenido a la API Banco Sangre")

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', home),  # Ruta raíz

    path('api/mapa/donadores/', donadores_para_mapa),
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas específicas por app
    path('api/rol/', include('rol.api.urls')),
    path('api/municipio/', include('municipio.api.urls')),
    path('api/colonia/', include('colonia.api.urls')),
    path('api/coordenada/', include('coordenada.api.urls')),
    path('api/direccion/', include('direccion.api.urls')),
    path('api/donador/', include('donador.api.urls')),

    # Eliminada la inclusión duplicada de 'usuario.api.urls' para evitar conflictos
    # path('api/', include('usuario.api.urls')),  # Comentar o eliminar si hay conflicto con router

    path('api/cita/', include('cita.api.urls')),  # Solo una vez
]
