# Generated by Django 3.0.6 on 2020-06-02 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersistema',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
