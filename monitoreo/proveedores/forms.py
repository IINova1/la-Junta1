from django import forms
from .models import Proveedor
import re

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: 12.345.678-9', 
                'id': 'id_rut'
            }),
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '+56 9 1234 5678'
            }),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'rubro': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ej: Distribuidora, Bebidas, Snacks...'
            }),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not rut:
            raise forms.ValidationError("El RUT es obligatorio.")
        if not re.match(r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$', rut):
            raise forms.ValidationError("Formato de RUT inválido. Ej: 12.345.678-9")
        if Proveedor.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este RUT ya está registrado.")
        return rut

    def clean_nombre_empresa(self):
        nombre_empresa = self.cleaned_data.get('nombre_empresa')
        if not nombre_empresa or nombre_empresa.strip() == "":
            raise forms.ValidationError("El nombre de la empresa es obligatorio.")
        if Proveedor.objects.filter(nombre_empresa__iexact=nombre_empresa).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un proveedor con este nombre.")
        return nombre_empresa.strip()

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono and not re.match(r'^\+?\d[\d\s\-]{7,14}$', telefono):
            raise forms.ValidationError("Teléfono inválido. Ej: +56 9 1234 5678")
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        if Proveedor.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email
