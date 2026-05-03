from django.db import models


class ContadorVisitas(models.Model):
    nombre = models.CharField(max_length=50, unique=True, default='sitio')
    total_visitas = models.PositiveIntegerField(default=0)
    visitantes_unicos = models.PositiveIntegerField(default=0)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'contador de visitas'
        verbose_name_plural = 'contadores de visitas'

    def __str__(self):
        return f"{self.nombre}: {self.total_visitas} visitas"
