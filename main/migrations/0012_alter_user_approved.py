# Generated by Django 5.0.6 on 2024-06-25 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_bookingtransaction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
