# Generated by Django 3.0.6 on 2020-06-02 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cestock', '0020_auto_20200601_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informe_medicamento',
            name='id_tipo_informe',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
        migrations.DeleteModel(
            name='Informe_Medicamento',
        ),
        migrations.DeleteModel(
            name='Tipo_Informe',
        ),
    ]