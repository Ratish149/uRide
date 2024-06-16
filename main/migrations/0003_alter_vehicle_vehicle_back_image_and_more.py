# Generated by Django 5.0.6 on 2024-06-16 08:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_vehicle_vehicle_door_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_back_image',
            field=models.ImageField(upload_to='vehicle/vehicle_images/'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_front_image',
            field=models.ImageField(upload_to='vehicle/vehicle_images/'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_left_image',
            field=models.ImageField(upload_to='vehicle/vehicle_images/'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_right_image',
            field=models.ImageField(upload_to='vehicle/vehicle_images/'),
        ),
        migrations.CreateModel(
            name='BookingTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('rented_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.vehicle')),
            ],
        ),
    ]
