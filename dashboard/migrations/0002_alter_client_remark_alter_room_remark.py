# Generated by Django 4.2.6 on 2023-11-26 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]