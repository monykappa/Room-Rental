# Generated by Django 4.2.6 on 2023-11-27 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0027_alter_utilities_previous_water'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlyrentalfee',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
