from django.urls import path
from . import views

urlpatterns = [
    # Vistas de Página Completa
    path('', views.home_view, name='home'),
    path('arquetipos/', views.arquetipos_lista_view, name='arquetipos_lista'),
    path('acerca-de/', views.acerca_de_view, name='acerca_de'),
    
    # Endpoints de API para el Globo / Mapa Interactivo (Retornan JSON)
    path('api/seres/', views.api_lista_seres, name='api_lista_seres'),
    path('api/pais/<str:codigo_iso>/seres/', views.api_seres_por_pais, name='api_seres_por_pais'),
    path('api/ser/<int:ser_id>/', views.api_detalle_ser, name='api_detalle_ser'),
]
