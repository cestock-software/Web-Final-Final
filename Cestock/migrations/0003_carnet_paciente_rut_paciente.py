# Generated by Django 3.0.5 on 2020-04-25 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cestock', '0002_atencion_medica_nro_ficha'),
    ]

    operations = [
        migrations.AddField(
            model_name='carnet_paciente',
            name='rut_paciente',
            field=models.ForeignKey(db_column='rut_paciente', null=True, on_delete=django.db.models.deletion.CASCADE, to='Cestock.Paciente'),
        ),
    ]
