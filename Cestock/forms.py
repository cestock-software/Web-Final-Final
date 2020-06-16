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


# # ----------------------Forms Nico------------------------
# class CarnetForm(forms.ModelForm):

#     class Meta:
#         model = Carnet_Paciente

#         fields = [
#             'nro_ficha',
#             'rut_paciente',
#             'sector',
#             'prevision',
#             'grupo_sanguineo',
#             'cesfam',
#         ]

#         labels = {
#             'nro_ficha': 'Nro. Ficha',
#             'rut_paciente': 'Rut Paciente',
#             'sector': 'Sector',
#             'prevision': 'Previsión',
#             'grupo_sanguineo': 'Grupo Sanguíneo',
#             'cesfam': 'CESFAM',
#         }

#         widgets = {
#             'nro_ficha': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'rut_paciente': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'sector': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': '', 'style': 'text-transform: capitalize'}),
#             'prevision': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'grupo_sanguineo': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'cesfam': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#         }

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

# class PacienteForm(forms.ModelForm):

#     class Meta:
#         model = Paciente

#         fields = '__all__'

#         exclude = [
#             'rut_paciente', 
#             'nombre',
#             'ap_paterno', 
#             'ap_materno', 
#             'sexo',
#             'fecha_nacimiento',
#             'estado'
#         ]

#         labels = {
#             'direccion': 'Dirección',
#             'email': 'Correo',
#             'nro_celular': 'Nro. Celular',
#             'comuna': 'Comuna',
#             'nombre_familiar': 'Nombre del Familiar',
#             'nro_familiar': 'Nro. del Familiar',
#             'email_familiar': 'Correo  del Familiar'
#         }

#         widgets = {
#             'direccion': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'email': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'nro_celular': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'comuna': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': '', 'style': 'text-transform: capitalize'}),
#             'nombre_familiar': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'nro_familiar': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'email_familiar': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#         }


# # ----------------------Forms Alex------------------------

# class MedicamentoRecetadoForm(forms.ModelForm):

#     class Meta:
#         model = Medicamento_Recetado

#         fields = [
#             'id_medicamento',
#             'id_receta_medica',
#             'duracion',
#             'frecuencia',
#             'cantidad_recetada',
#         ]

#         labels = {
#             'id_medicamento': 'ID Medicamento',
#             'id_receta_medica': 'ID Receta',
#             'duracion': 'Duración',
#             'frecuencia': 'Frecuencia',
#             'cantidad_recetada': 'Cant. Recetada',
#         }

#         widgets = {
#             'id_receta_medica': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'id_medicamento': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'duracion': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'frecuencia': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#             'cantidad_recetada': forms.TextInput(attrs={'class': 'form-control-sm form-control', 'readonly': ''}),
#         } 