# Generated by Django 4.2.7 on 2023-12-07 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0056_utilities_current_water'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlyrentalfee',
            name='current_water',
        ),
    ]
