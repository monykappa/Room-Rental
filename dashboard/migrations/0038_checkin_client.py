# Generated by Django 4.2.7 on 2023-12-01 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0037_alter_room_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='check_in_entries', to='dashboard.client'),
        ),
    ]
