# Generated by Django 3.1.5 on 2021-01-08 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Portal', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='farmer_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='location',
            field=models.CharField(default='', max_length=100),
        ),
    ]