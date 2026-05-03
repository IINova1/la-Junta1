from django.db import models
from django.core.validators import MinLengthValidator

class Proveedor(models.Model):
    rut = models.CharField(
        max_length=12,
        unique=True,
        verbose_name='RUT',
    )
    nombre_empresa = models.CharField(
        max_length=150,
        verbose_name='Nombre Empresa',
        unique=True,
        validators=[MinLengthValidator(2, "El nombre de la empresa debe tener al menos 2 caracteres.")]
    )
    nombre_contacto = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nombre Contacto'
    )
    email = models.EmailField(
        unique=True,
        max_length=191,
        verbose_name='email address'
    )
    telefono = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name='Teléfono'
    )
    direccion = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Dirección'
    )
    rubro = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Rubro'
    )

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['nombre_empresa']

    def __str__(self):
        return self.nombre_empresa
