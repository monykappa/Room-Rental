# Generated by Django 4.2.6 on 2023-11-26 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_rename_ownername_houseowner_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='status',
            field=models.CharField(default='available', max_length=20),
        ),
    ]