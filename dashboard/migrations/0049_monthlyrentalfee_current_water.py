# Generated by Django 4.2.7 on 2023-12-03 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0048_remove_utilities_previous_water_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyrentalfee',
            name='current_water',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
