from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Validador genérico para campos numéricos no negativos
def no_negativo(value):
    if value is not None and value < 0:
        raise ValidationError('El valor no puede ser negativo.')

# --- Categoria ---
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Categorias'

    def __str__(self):
        return self.nombre

    def clean(self):
        if not self.nombre.strip():
            raise ValidationError({'nombre': 'El nombre no puede estar vacío.'})

# --- Nutricional ---
class Nutricional(models.Model):
    ingredientes = models.CharField(max_length=300, blank=True, null=True)
    tiempo_preparacion = models.CharField(max_length=100, blank=True, null=True)
    proteinas = models.CharField(max_length=45, blank=True, null=True)
    azucar = models.CharField(max_length=45, blank=True, null=True)
    gluten = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Nutricional'

    def __str__(self):
        return f"ingredientes {self.id}"

# --- Producto ---
class Producto(models.Model):
    codigo = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    costo = models.IntegerField(blank=True, null=True, validators=[no_negativo])
    precio = models.IntegerField(blank=True, null=True, validators=[no_negativo])
    caducidad = models.DateField()
    elaboracion = models.DateField(blank=True, null=True)
    tipo = models.CharField(max_length=100)
    Categorias = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, db_column='Categorias_id')
    Nutricional = models.ForeignKey(Nutricional, on_delete=models.DO_NOTHING, db_column='Nutricional_id')
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True, verbose_name='Imagen')
    stock_actual = models.IntegerField(blank=True, null=True, validators=[no_negativo])
    stock_minimo = models.IntegerField(blank=True, null=True, validators=[no_negativo])
    stock_maximo = models.IntegerField(blank=True, null=True, validators=[no_negativo])
    presentacion = models.CharField(max_length=100, blank=True, null=True)
    formato = models.CharField(max_length=100, blank=True, null=True)
    creado = models.DateTimeField(blank=True, null=True)
    modificado = models.DateTimeField(blank=True, null=True)
    eliminado = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Productos'

    def __str__(self):
        return self.nombre

    def clean(self):
        errors = {}
        # Nombre obligatorio
        if not self.nombre.strip():
            errors['nombre'] = 'El nombre no puede estar vacío.'

        # Precio no negativo
        if self.precio is not None and self.precio < 0:
            errors['precio'] = 'El precio no puede ser negativo.'

        if self.costo is not None and self.costo < 0:
            errors['costo'] = 'El costo no puede ser negativo.'

        # Caducidad mayor que elaboración si existe
        if self.elaboracion and self.caducidad and self.caducidad < self.elaboracion:
            errors['caducidad'] = 'La caducidad no puede ser anterior a la fecha de elaboración.'

        # Stock coherente
        if self.stock_minimo and self.stock_maximo and self.stock_minimo > self.stock_maximo:
            errors['stock_minimo'] = 'El stock mínimo no puede ser mayor que el stock máximo.'

        if errors:
            raise ValidationError(errors)

# --- ReglaAlertaVencimiento ---
class ReglaAlertaVencimiento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    dias_anticipacion = models.IntegerField(validators=[no_negativo])

    def __str__(self):
        return self.nombre

# --- ProductoReglaAlerta ---
class ProductoReglaAlerta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    regla = models.ForeignKey(ReglaAlertaVencimiento, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'regla')

    def __str__(self):
        return f"{self.producto.nombre} - {self.regla.nombre}"
