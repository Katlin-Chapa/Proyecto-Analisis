# Generated by Django 5.1.2 on 2024-10-25 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventario', '0006_alter_stock_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
