# Generated by Django 4.2.7 on 2023-12-03 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0049_monthlyrentalfee_current_water'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlyrentalfee',
            name='water_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
