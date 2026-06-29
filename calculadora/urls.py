from django.urls import path
from . import views

urlpatterns = [
    # Esta ruta cargará nuestro formulario como la página principal de la app
    path('', views.calcular_cobertura_view, name='calcular_cobertura'),
]