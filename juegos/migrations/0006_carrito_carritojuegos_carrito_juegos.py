# Generated by Django 5.1.1 on 2024-09-17 00:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('juegos', '0005_delete_categoria'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CarritoJuegos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juegos.carrito')),
                ('juego', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juegos.juego')),
            ],
        ),
        migrations.AddField(
            model_name='carrito',
            name='juegos',
            field=models.ManyToManyField(through='juegos.CarritoJuegos', to='juegos.juego'),
        ),
    ]
