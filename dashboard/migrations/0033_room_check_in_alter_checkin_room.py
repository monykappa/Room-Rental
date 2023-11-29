# Generated by Django 4.2.6 on 2023-11-29 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_monthlyrentalfee_water_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='check_in',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='room_check_in', to='dashboard.checkin'),
        ),
        migrations.AlterField(
            model_name='checkin',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_in_entries', to='dashboard.room'),
        ),
    ]
