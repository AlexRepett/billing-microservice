from django.urls import path
from . import views

urlpatterns = [
    # Al estar vacío el primer parámetro, se convierte en la raíz de la app
    path('', views.home, name='home'),
]