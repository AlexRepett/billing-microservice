from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse
import re

class Cliente(models.Model):
    # 1. Campos del modelo (13 campos)
    rfc = models.CharField(
        max_length=13, 
        unique=True,
        db_index=True,
        help_text="RFC del cliente (12 o 13 caracteres)")
    razon_social = models.CharField(
        max_length=255,
        help_text="Razón social del cliente")
    email = models.EmailField(
        max_length=255, 
        help_text="Correo electrónico del cliente")
    telefono = models.CharField(
        max_length=20,
        blank=True,
        help_text="Teléfono del cliente")
    direccion = models.TextField(
        blank=True, 
        help_text="Dirección completa (calle, número, colonia)")
    codigo_postal = models.CharField(
        max_length=10,
        blank=True,  # ← Agregar (es opcional)
    help_text="Código postal")
    ciudad = models.CharField(
        max_length=100, 
        blank=True)  
    estado = models.CharField(
        max_length=100, 
        blank=True) 
    pais = models.CharField(
        max_length=100, 
        default='México')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    # 2. Meta class (opciones del modelo)
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["-fecha_registro"]
        db_table = "clientes"
    # 3. Método __str__
    def __str__(self):
        return f"{self.razon_social} ({self.rfc})"
    def get_absolute_url(self):
        return reverse('cliente-detail', kwargs={'pk': self.pk})
    # 4. Métodos personalizados
    def get_facturas_activas(self):
        """
        Retorna todas las facturas NO canceladas de este cliente.
        """
        return self.facturas.exclude(estatus='CANCELADA')
    def clean(self):
        """
        Valida que el RFC tenga formato mexicano válido.
        """
        # Llamar al clean() del padre (siempre hazlo)
        super().clean()
        
        # Convertir RFC a mayúsculas
        if self.rfc:
            self.rfc = self.rfc.upper().strip()
            
            # Patrón de RFC mexicano
            # Persona Moral: 3 letras + 6 dígitos + 3 caracteres (12 total)
            # Persona Física: 4 letras + 6 dígitos + 3 caracteres (13 total)
            patron_rfc = r'^[A-ZÑ&]{3,4}[0-9]{6}[A-Z0-9]{3}$'
            
            if not re.match(patron_rfc, self.rfc):
                raise ValidationError({
                    'rfc': 'El RFC no tiene un formato válido. Debe tener 12 o 13 caracteres (ej: ABC123456XYZ o ABCD123456XYZ).'
                })
