from django import forms
from .models import Producto, Categoria
from django.core.exceptions import ValidationError

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'codigo', 'nombre', 'descripcion', 'marca', 'costo', 'precio', 'caducidad',
            'elaboracion', 'tipo', 'Categorias', 'Nutricional',
            'stock_actual', 'stock_minimo', 'stock_maximo', 
            'presentacion', 'formato', 'imagen'
        ]
        # --- CORRECCIÓN APLICADA AQUÍ ---
        widgets = {
            # Se agrega format='%Y-%m-%d' para que el input date de HTML5 cargue el valor correctamente al editar
            'caducidad': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'elaboracion': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError('El nombre no puede estar vacío.')
        return nombre

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise ValidationError('El precio no puede ser negativo.')
        return precio

    def clean_costo(self):
        costo = self.cleaned_data.get('costo')
        if costo is not None and costo < 0:
            raise ValidationError('El costo no puede ser negativo.')
        return costo

    def clean(self):
        cleaned_data = super().clean()
        stock_minimo = cleaned_data.get("stock_minimo")
        stock_maximo = cleaned_data.get("stock_maximo")
        stock_actual = cleaned_data.get("stock_actual")
        caducidad = cleaned_data.get("caducidad")
        elaboracion = cleaned_data.get("elaboracion")

        # Validaciones de stock
        if stock_minimo is not None and stock_maximo is not None:
            if stock_minimo >= stock_maximo:
                raise forms.ValidationError(
                    "Error de lógica: El stock mínimo no puede ser mayor o igual al stock máximo."
                )
        if stock_actual is not None and stock_minimo is not None and stock_maximo is not None:
            if not (stock_minimo <= stock_actual <= stock_maximo):
                raise forms.ValidationError(
                    "Error de consistencia: El stock actual debe estar entre los valores de stock mínimo y máximo."
                )

        # Validación de fechas
        if elaboracion and caducidad:
            if caducidad < elaboracion:
                raise forms.ValidationError(
                    "La caducidad no puede ser anterior a la fecha de elaboración."
                )

        return cleaned_data


class ImportarInventarioEleventaForm(forms.Form):
    archivo = forms.FileField(
        label='Archivo de inventario',
        help_text='Sube un archivo .xlsx, .xlsm o .csv exportado desde eleventa.',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xlsm,.csv',
        })
    )

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise ValidationError('El nombre de la categoría no puede estar vacío.')
        return nombre
