# Generated by Django 4.2.7 on 2023-12-03 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0047_remove_utilities_previous_date_utilities_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilities',
            name='previous_water_quantity',
        ),
    ]
