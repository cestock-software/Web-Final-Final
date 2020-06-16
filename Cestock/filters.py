import django_filters
from django_filters import CharFilter
from .models import *

class MedicamentoFilter(django_filters.FilterSet):
    nombre_medicamento = CharFilter(label='Buscar Por Nombre Medicamento: ',field_name='nombre_medicamento', lookup_expr='icontains')

    class Meta:
        model = Medicamento
        fields = ['nombre_medicamento']


class PacienteFilter(django_filters.FilterSet):
    nombre = CharFilter(label='Buscar Por Nombre Paciente: ',field_name='nombre', lookup_expr='icontains')
    class Meta:
        model = Paciente
        fields = ['nombre']

class AtencionFilter(django_filters.FilterSet):
    nro_ficha = CharFilter(label='Buscar Por Nro Ficha:', field_name='nro_ficha')

    class Meta:
        model = Atencion_Medica
        fields = ['nro_ficha'] 