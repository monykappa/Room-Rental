# Generated by Django 4.2.6 on 2023-11-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_parking_parkingqty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='ParkingQty',
            field=models.IntegerField(null=True),
        ),
    ]
