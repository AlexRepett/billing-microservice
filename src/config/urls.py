from django.contrib import admin
from django.urls import path, include # Importa 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Esta línea conecta la raíz (http://127.0.0.1:8000/) con tu app billing
    path('', include('billing.urls')), 
]