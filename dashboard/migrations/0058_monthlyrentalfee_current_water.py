# Generated by Django 4.2.7 on 2023-12-07 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0057_remove_monthlyrentalfee_current_water'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyrentalfee',
            name='current_water',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]