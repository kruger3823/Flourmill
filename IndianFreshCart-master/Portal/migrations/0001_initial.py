# Generated by Django 3.1.5 on 2021-01-07 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('usertype', models.CharField(choices=[('1', 'Customer'), ('2', 'Farmer')], default='1', max_length=10)),
                ('gender', models.CharField(choices=[('1', 'Male'), ('2', 'Female'), ('3', 'Other')], default='1', max_length=10)),
                ('date_of_birth', models.CharField(default='', max_length=10)),
                ('city', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='', max_length=70)),
                ('country', models.CharField(default='', max_length=50)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
