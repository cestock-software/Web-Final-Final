# Generated by Django 3.0.5 on 2020-04-25 07:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cestock', '0006_auto_20200425_0358'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicamento_recetado',
            name='id_medicamento',
            field=models.ForeignKey(db_column='id_medicamento', null=True, on_delete=django.db.models.deletion.CASCADE, to='Cestock.Medicamento'),
        ),
        migrations.AddField(
            model_name='medicamento_recetado',
            name='id_receta_medica',
            field=models.ForeignKey(db_column='id_receta_medica', null=True, on_delete=django.db.models.deletion.CASCADE, to='Cestock.Receta_Medica'),
        ),
    ]