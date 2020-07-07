from django import forms
from .models import *
from django.contrib.auth import get_user_model
from users.models import *
from django.contrib.auth.forms import AuthenticationForm,ReadOnlyPasswordHashField
from django.contrib.admin.forms import AdminPasswordChangeForm


User = get_user_model()

class LoginForm(forms.ModelForm):
    ''' Formulario para el login '''
    rut = forms.CharField(
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'username',
            'class': 'form-control mb-4'
        })
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña',
            'class': 'form-control mb-4 '
        }),
    )

    class Meta:
        model = UserSistema
        fields =['rut','password']

class FormAtencion(forms.ModelForm):
    class Meta:
        model=Atencion_Medica
        fields = (
            'nro_ficha', 'nombre_medico'
        )
        labels = {
            'nombre_medico': ('Nombre médico'),
            'nro_ficha': ('Número de ficha'),
        }
        widgets = {
            'nombre_medico': forms.TextInput(attrs={
                'class': 'form-control responsive',
                'placeholder': 'Ingrese Nombre de Médico',
                'required': True,

            }),
            'nro_ficha': forms.Select(attrs={
                'class': 'form-control responsive',
                'placeholder': 'Ingrese Número de Ficha',
                'required': True,
            }),
        }

    def clean_nro_ficha(self):
            nro_ficha = self.cleaned_data['nro_ficha']
            fichas = Carnet_Paciente.objects.filter(nro_ficha__iexact=nro_ficha)
            if self.instance:
                fichas = fichas.exclude(id=self.instance.id)
            if fichas.count() is None:
                raise ValidationError('Lo sentimos, pero esta ficha no existe')
            else:
                return nro_ficha


class FormPrescripcion(forms.ModelForm):
    class Meta:
        model=Detalle_Atencion
        fields = (
            'sintomas', 'diagnostico','tratamiento','observacion'
        )
        labels = {
            'sintomas': ('Síntomas'),
            'diagnostico': ('Diagnóstico'),
            'tratamiento': ('Tratamiento'),
            'observacion': ('Observación'),
        }

        widgets = {
            'sintomas': forms.Textarea(attrs={
                'rows': '3',
                'class': 'textotal form-control',
                'placeholder': 'Ingrese Sintomas del Paciente..',
                'required': True,
            }),
            'diagnostico': forms.Textarea(attrs={
                'rows': '3',
                'class': 'textotal form-control',
                'placeholder': 'Ingrese Diagnostico del Paciente..',
                'required': True,
            }),
            'tratamiento': forms.Textarea(attrs={
                'rows': '3',
                'class': 'textotal form-control',
                'placeholder': 'Ingrese Tratamiento para el Paciente..',
                'required': True,
            }),
            'observacion': forms.Textarea(attrs={
                'rows': '3',
                'class': 'textotal form-control',
                'placeholder': 'Ingrese Observacion..',
            }),
        }




class DetalleAtencionForm(forms.ModelForm):

    class Meta:
        model = Detalle_Atencion

        fields = '__all__'

        exclude = ['atencion_medica']

        labels = {
            'sintomas': 'Síntomas',
            'diagnostico': 'Diagnóstico',
            'tratamiento': 'Tratamiento',
            'observacion': 'Observación',
        }

        widgets = {
            'sintomas': forms.Textarea(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
            'observacion': forms.Textarea(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
        }

