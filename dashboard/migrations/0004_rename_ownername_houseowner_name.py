# Generated by Django 4.2.6 on 2023-11-26 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_rename_name_client_clientname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='houseowner',
            old_name='OwnerName',
            new_name='name',
        ),
    ]
