# Generated by Django 2.2.13 on 2022-08-30 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220830_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='code',
            field=models.CharField(choices=[('knowledge', 'مدیریت دانش'), ('center', 'رشد، خلاقیت و نوآوری'), ('resume', 'آموزش و امور محققین'), ('future', 'آینده پژوهی')], max_length=30),
        ),
    ]
