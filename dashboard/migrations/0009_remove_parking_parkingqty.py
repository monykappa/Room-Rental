# Generated by Django 4.2.6 on 2023-11-26 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_parking_remark'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parking',
            name='ParkingQty',
        ),
    ]
