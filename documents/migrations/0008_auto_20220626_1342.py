# Generated by Django 2.2.13 on 2022-06-26 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_auto_20220626_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='field',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
