# Generated by Django 4.0.5 on 2022-09-03 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0012_info'),
    ]

    operations = [
        migrations.RenameField(
            model_name='info',
            old_name='Mob',
            new_name='mob',
        ),
    ]
