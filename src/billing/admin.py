from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('rfc', 'razon_social', 'email', 'ciudad', 'activo', 'fecha_registro')
    list_filter = ('activo', 'pais', 'estado')
    search_fields = ('rfc', 'razon_social', 'email')
    ordering = ('-fecha_registro',)
    readonly_fields = ('fecha_registro',)
    
    fieldsets = (
        ('Información Fiscal', {
            'fields': ('rfc', 'razon_social')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono')
        }),
        ('Ubicación', {
            'fields': ('direccion', 'codigo_postal', 'ciudad', 'estado', 'pais')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_registro')
        }),
    )