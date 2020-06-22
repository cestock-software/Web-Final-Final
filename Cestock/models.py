from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from datetime import datetime
import datetime
# Create your models here.

class Atencion_Medica(models.Model):
    nro_ficha = models.ForeignKey('Carnet_Paciente', db_column='nro_ficha',on_delete=models.CASCADE, null=True)
    fecha_atencion_medica = models.DateField(auto_now=True)
    nombre_medico = models.CharField(default="",max_length=255, blank=True, null=True)
    fecha_prox_atencion = models.DateField(auto_now=True,blank=True, null=True)

    class Meta:
        db_table = 'atencion_medica'
        verbose_name = 'Atención Medica'
        verbose_name_plural = 'Atenciones Medicas'
    
    def __str__(self):
        return f'{self.nombre_medico}'

class Carnet_Paciente(models.Model):
    nro_ficha = models.IntegerField(primary_key=True)
    rut_paciente = models.ForeignKey('Paciente', db_column='rut_paciente', on_delete=models.CASCADE, null=True)
    id_sector = models.ForeignKey('Sector', db_column='id_sector', on_delete=models.CASCADE, null=True)
    id_prevision = models.ForeignKey('Prevision', db_column='id_prevision', on_delete=models.CASCADE, null=True)
    id_grupo = models.ForeignKey('Grupo_sanguineo', db_column='id_grupo', on_delete=models.CASCADE, null=True)
    id_cesfam = models.ForeignKey('Cesfam', db_column='id_cesfam', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'carnet_paciente'
        verbose_name = 'Carnet Paciente'
        verbose_name_plural = 'Carnet Pacientes'
    
    def __str__(self):
        return f'{self.nro_ficha}'

class Detalle_Atencion(models.Model):
    atencion_medica = models.ForeignKey('Atencion_Medica',on_delete=models.CASCADE,blank=True, null=True)
    sintomas = models.CharField(default="",max_length=255, blank=True, null=True)
    diagnostico = models.CharField(default="",max_length=255, blank=True, null=True)
    tratamiento = models.CharField(default="",max_length=255, blank=True, null=True)
    observacion = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'detalle_atencion'
        verbose_name = 'Detalle Atención'
        verbose_name_plural = 'Detalle Atenciones'

    def __str__(self):
        return f'{self.sintomas}'

class Entrega(models.Model):
    id_entrega_medicamento = models.IntegerField(primary_key=True)
    fecha_entrega = models.DateField(auto_now=True,blank=True, null=True)
    fecha_proxima_entrega = models.DateField(auto_now=True,blank=True, null=True)
    nombre_farmaceutico = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'entrega'
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'

    def __str__(self):
        return f'{self.id_entrega_medicamento}' 

class Error(models.Model):
    id_error = models.IntegerField(primary_key=True)
    nro_error = models.IntegerField(default=0,blank=True, null=True)
    codigo_error = models.CharField(default="",max_length=255, blank=True, null=True)
    fecha_hora_error = models.DateField(auto_now=True,blank=True, null=True)
    lugar_error = models.CharField(default="",max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=1,blank=True, null=True)

    class Meta:
        db_table = 'error'
        verbose_name = 'Error'
        verbose_name_plural = 'Errores'

    def __str__(self):
        return f'{self.id_error}'
    
class Estado_Reserva(models.Model):
    id_estado_reserva = models.CharField(primary_key=True, max_length=255)
    tipo_estado = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'estado_reserva'
        verbose_name = 'Estado Reserva'
        verbose_name_plural = 'Estado Reservas'

    def __str__(self):
        return f'{self.id_estado_reserva}' 

class Medicamento(models.Model):
    id_medicamento = models.IntegerField(primary_key=True)
    id_estado = models.ForeignKey('Estado', db_column='id_estado', on_delete=models.CASCADE, null=True)
    nombre_medicamento = models.CharField(default=0,max_length=255, blank=True, null=True)
    dosis = models.IntegerField(default=0, blank=True, null=True)
    id_umedida = models.ForeignKey('Unidad_medida', db_column='id_umedida', on_delete=models.CASCADE, null=True)
    id_formato = models.ForeignKey('Formato', db_column='id_formato', on_delete=models.CASCADE, null=True)
    id_laboratorio = models.ForeignKey('Laboratorio', db_column='id_laboratorio', on_delete=models.CASCADE, null=True)
    total_disponible = models.IntegerField(default=0,blank=True, null=True)
    total_reservado = models.IntegerField(default=0,blank=True, null=True)
    total_retirado = models.IntegerField(default=0,blank=True, null=True)

    class Meta:
        db_table = 'medicamento'
        verbose_name = 'Medicamento'
        verbose_name_plural = 'Medicamentos'

    def __str__(self):
        return f'{self.id_medicamento}' 

class Medicamento_Entregado(models.Model):
    id_entrega_medicamento = models.ForeignKey('Entrega', db_column='id_entrega_medicamento', on_delete=models.CASCADE, null=True)
    id_medicamento_recetado = models.ForeignKey('Medicamento_Recetado', db_column='id_medicamento_recetado', on_delete=models.CASCADE, null=True)
    cantidad_entregada = models.IntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'medicamento_entregado'
        verbose_name = 'Medicamento Entregado'
        verbose_name_plural = 'Medicmentos Entregados'

    def __str__(self):
        return f'{self.id_entrega_medicamento}'
    
class Medicamento_Recetado(models.Model):
    id_medicamento_recetado = models.IntegerField(primary_key=True,null=True)
    id_medicamento = models.ForeignKey('Medicamento', db_column='id_medicamento', on_delete=models.CASCADE, null=True)
    id_receta_medica = models.ForeignKey('Receta_Medica', db_column='id_receta_medica', on_delete=models.CASCADE, null=True)
    id_estado_reserva = models.ForeignKey('Estado_Reserva', db_column='id_estado_reserva', on_delete=models.CASCADE, null=True)
    duracion = models.CharField(default="",max_length=255, blank=True, null=True)
    frecuencia = models.CharField(default="",max_length=255, blank=True, null=True)
    cantidad_recetada = models.IntegerField()

    class Meta:
        db_table = 'medicamento_recetado'
        verbose_name = 'Medicamento Recetado'
        verbose_name_plural = 'Medicamentos Recetados'

    def __str__(self):
        return f'{self.id_medicamento_recetado}'
    

class Paciente(models.Model):
    rut_paciente = models.CharField(primary_key=True, max_length=255)
    nombre = models.CharField(default="",max_length=255, blank=True, null=True)
    ap_paterno = models.CharField(default="",max_length=255, blank=True, null=True)
    ap_materno = models.CharField(default="",max_length=255, blank=True, null=True)
    direccion = models.CharField(default="",max_length=255, blank=True, null=True)
    email = models.CharField(default="",max_length=255, blank=True, null=True)
    nro_celular = models.CharField(default="",max_length=255, blank=True, null=True)
    fecha_nacimiento = models.DateField(auto_now=False,null=True)
    nro_tutor = models.CharField(default="",max_length=255, blank=True, null=True)
    email_tutor = models.CharField(default="",max_length=255, blank=True, null=True)
    id_genero = models.ForeignKey('Genero', db_column='id_genero', on_delete=models.CASCADE, null=True)
    id_comuna = models.ForeignKey('Comuna', db_column='id_comuna', on_delete=models.CASCADE, null=True)
    id_estado = models.ForeignKey('Estado', db_column='id_estado', on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = 'paciente'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f'{self.rut_paciente}' 

class Recordatorio(models.Model):
    id_recordatorio = models.IntegerField(primary_key=True)
    nombre_medicamento = models.CharField(default="",max_length=255,blank=True, null=True)
    nombre_paciente = models.CharField(default="",max_length=255,blank=True, null=True)
    email_paciente = models.CharField(default="",max_length=255,blank=True, null=True)
    celular_paciente = models.CharField(default="",max_length=255,blank=True, null=True)
    celular_tutor = models.CharField(default="",max_length=255,blank=True, null=True)
    email_tutor = models.CharField(default="",max_length=255,blank=True, null=True)
    fecha_retiro = models.DateField(blank=True, null=True)
    estado_sms = models.CharField(default="",max_length=255,blank=True, null=True)
    estado_email = models.CharField(default="",max_length=255,blank=True, null=True)
    cesfam = models.CharField(default="",max_length=255,blank=True, null=True)

    class Meta:
        db_table = 'recordatorio'
        verbose_name = 'Recordatorio'
        verbose_name_plural = 'Recordatorios'

    def __str__(self):
        return f'{self.id_recordatorio}' 

class Tipo_Retiro(models.Model):
    id_tipo_retiro = models.IntegerField(primary_key=True)
    descripcion_retiro = models.CharField(default="",max_length=255)

    class Meta:
        db_table = 'tipo_retiro'
        verbose_name = 'Tipo Retiro'
        verbose_name_plural = 'Tipo Retiros'

    def __str__(self):
        return f'{self.id_tipo_retiro}'


class Receta_Medica(models.Model):
    id_receta_medica = models.IntegerField(primary_key=True)
    atencion_medica = models.ForeignKey('Atencion_Medica', db_column='id',null=True,on_delete=models.CASCADE)

    class Meta:
        db_table = 'receta_medica'
        verbose_name = 'Receta Médica'
        verbose_name_plural = 'Recetas Médicas'

    def __str__(self):
        return f'{self.id_receta_medica}' 

class Reposicion(models.Model):
    id_reposicion = models.IntegerField(primary_key=True)
    id_medicamento = models.ForeignKey('Medicamento', db_column='id_medicamento',on_delete=models.CASCADE, null=True)
    cantidad_repuesta = models.FloatField( default=0,blank=True, null=True)
    fecha_reposicion = models.DateField(default=datetime.date.today, null=False)
    fecha_vencimiento = models.DateField(default=datetime.date.today, null=False)
    nombre_farmaceutico = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'reposicion'
        verbose_name = 'Reposición'
        verbose_name_plural = 'Repocisiones'
    
    def __str__(self):
        return f'{self.id_reposicion}' 

class Reserva(models.Model):
    id_reserva = models.IntegerField(primary_key=True)
    id_medicamento_recetado = models.ForeignKey('Medicamento_Recetado', db_column='id_medicamento_recetado', on_delete=models.CASCADE, null=True)
    id_estado_reserva = models.ForeignKey('Estado_Reserva', db_column='id_estado_reserva', on_delete=models.CASCADE, null=True)
    cant_reservada = models.IntegerField(default=0,blank=True, null=True)
    fecha_reserva = models.DateField(auto_now=True)
    fecha_retiro = models.DateField(auto_now=True,blank=True, null=True)

    class Meta:
        db_table = 'reserva'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'{self.id_reserva}' 

class retiro_medicamento(models.Model):
    id_retiro = models.IntegerField(primary_key=True)
    id_medicamento = models.IntegerField(default=0, blank=True, null=True)
    id_tipo_retiro = models.IntegerField(default=0, blank=True, null=True)
    cantidad_retirada = models.IntegerField(default=0, blank=True, null=True)
    fecha_retiro = models.DateField(auto_now=True,blank=True, null=True)
    class Meta:
        db_table = 'retiro_medicamento'
        verbose_name = 'retiro_medicamento'
        verbose_name_plural = 'retiro_medicamento'

    def __str__(self):
        return f'{self.id_retiro}' 

class Genero(models.Model):
    id_genero = models.IntegerField(primary_key=True)
    tipo_genero = models.CharField(default="",max_length=255)

    class Meta:
        db_table = 'genero'
        verbose_name = 'Tipo Genero'
        verbose_name_plural = 'Tipo Generos'

    def __str__(self):
        return f'{self.id_genero}'

class Comuna(models.Model):
    id_comuna = models.IntegerField(primary_key=True)
    nombre_comuna = models.CharField(default="",max_length=255)

    class Meta:
        db_table = 'comuna'
        verbose_name = 'Nombre Comuna'
        verbose_name_plural = 'Nombre Comunas'

    def __str__(self):
        return f'{self.id_comuna}'

class Cesfam(models.Model):
    id_cesfam = models.IntegerField(primary_key=True)
    nombre_cesfam = models.CharField(default="",max_length=255, blank=True, null=True)
    id_comuna = models.ForeignKey('Comuna', db_column='id_comuna', on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = 'cesfam'
        verbose_name = 'Nombre Cesfam'
        verbose_name_plural = 'Nombre Cesfams'

    def __str__(self):
        return f'{self.id_cesfam}'

class Prevision(models.Model):
    id_prevision = models.IntegerField(primary_key=True)
    tipo_prevision = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'prevision'
        verbose_name = 'Tipo Previsión'
        verbose_name_plural = 'Tipo Previsiones'

    def __str__(self):
        return f'{self.id_prevision}'

class Grupo_sanguineo(models.Model):
    id_grupo = models.IntegerField(primary_key=True)
    tipo_grupo = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'grupo_sanguineo'
        verbose_name = 'Tipo Grupo Sanguineo'
        verbose_name_plural = 'Tipo Grupo Sanguineos'

    def __str__(self):
        return f'{self.id_grupo}'

class Sector(models.Model):
    id_sector = models.IntegerField(primary_key=True)
    nombre_sector = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'sector'
        verbose_name = 'Nombre Sector'
        verbose_name_plural = 'Nombre Sectores'

    def __str__(self):
        return f'{self.id_sector}'

class Estado(models.Model):
    id_estado = models.IntegerField(primary_key=True)
    tipo_estado = models.CharField(default="",max_length=255)

    class Meta:
        db_table = 'estado'
        verbose_name = 'Tipo Estado'
        verbose_name_plural = 'Tipo Estados'

    def __str__(self):
        return f'{self.id_estado}'

class Formato(models.Model):
    id_formato = models.IntegerField(primary_key=True)
    nombre_formato = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'formato'
        verbose_name = 'Nombre Formato'
        verbose_name_plural = 'Nombre Formatos'

    def __str__(self):
        return f'{self.id_formato}'

class Laboratorio(models.Model):
    id_laboratorio = models.IntegerField(primary_key=True)
    nombre_laboratorio = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'laboratorio'
        verbose_name = 'Nombre Laboratorio'
        verbose_name_plural = 'Nombre Laboratorios'

    def __str__(self):
        return f'{self.id_laboratorio}'

class Unidad_medida(models.Model):
    id_umedida = models.IntegerField(primary_key=True)
    tipo_medida = models.CharField(default="",max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'unidad_medida'
        verbose_name = 'Tipo Medida'
        verbose_name_plural = 'Tipo Medidas'

    def __str__(self):
        return f'{self.id_umedida}'
