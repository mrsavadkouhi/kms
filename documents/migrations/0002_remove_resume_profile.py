# Generated by Django 2.2.13 on 2022-06-27 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resume',
            name='profile',
        ),
    ]
