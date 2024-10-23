# Generated by Django 5.1.2 on 2024-10-23 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('cantidad', models.IntegerField(default=1)),
                ('fecha_vencimiento', models.DateField()),
                ('fecha_ingreso', models.DateField(auto_now_add=True)),
                ('numero_documento', models.CharField(blank=True, max_length=50, null=True)),
                ('dosis', models.CharField(max_length=50)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='imagenes/')),
                ('es_eliminado', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inventario.categoria')),
            ],
        ),
    ]
