# Generated by Django 2.2.13 on 2022-08-12 07:42

from django.db import migrations, models
import documents.models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_auto_20220805_1509'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='avatar',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to=documents.models.get_avatar_directory_path),
        ),
    ]