# Generated by Django 3.0.6 on 2020-06-02 00:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cestock', '0023_auto_20200601_2020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carnet_paciente',
            name='cesfam',
        ),
        migrations.RemoveField(
            model_name='carnet_paciente',
            name='grupo_sanguineo',
        ),
        migrations.RemoveField(
            model_name='carnet_paciente',
            name='prevision',
        ),
        migrations.RemoveField(
            model_name='carnet_paciente',
            name='sector',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='formato',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='gr_ml',
        ),
        migrations.RemoveField(
            model_name='medicamento',
            name='laboratorio',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='comuna',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nombre_familiar',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='sexo',
        ),
    ]
