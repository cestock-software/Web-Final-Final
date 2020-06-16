# Generated by Django 3.0.5 on 2020-04-30 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cestock', '0013_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='retiro_medicamento',
            fields=[
                ('id_retiro', models.IntegerField(primary_key=True, serialize=False)),
                ('id_medicamento', models.IntegerField(blank=True, default=0, null=True)),
                ('id_tipo_retiro', models.IntegerField(blank=True, default=0, null=True)),
                ('cantidad_retirada', models.IntegerField(blank=True, default=0, null=True)),
                ('fecha_retiro', models.DateField(auto_now=True, null=True)),
            ],
            options={
                'verbose_name': 'retiro_medicamento',
                'verbose_name_plural': 'retiro_medicamento',
                'db_table': 'retiro_medicamento',
            },
        ),
        migrations.CreateModel(
            name='tipo_retiro',
            fields=[
                ('id_tipo_retiro', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion_retiro', models.CharField(blank=True, default='', max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'tipo_retiro',
                'verbose_name_plural': 'tipo_retiro',
                'db_table': 'tipo_retiro',
            },
        ),
        migrations.RenameField(
            model_name='receta_medica',
            old_name='id_receta',
            new_name='id_receta_medica',
        ),
    ]