# Generated by Django 4.2.7 on 2023-12-01 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0039_alter_checkin_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='contact',
            field=models.IntegerField(max_length=200),
        ),
    ]
