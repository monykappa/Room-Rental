# Generated by Django 4.2.7 on 2023-12-09 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0058_monthlyrentalfee_current_water'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyrentalfee',
            name='previous_water',
            field=models.PositiveIntegerField(default=0),
        ),
    ]