# Generated by Django 5.1.7 on 2025-03-25 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mesas', '0003_mesa_id_pedido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesa',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
