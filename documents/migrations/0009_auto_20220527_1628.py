# Generated by Django 2.2.13 on 2022-05-27 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0008_auto_20220527_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='future',
            name='future_type',
            field=models.CharField(choices=[('Rasadi', 'گزارش رصدی'), ('Info', 'اینفوگرافی'), ('Dide', 'دیده بان'), ('Organ', 'گزارش سازمانی')], max_length=255),
        ),
    ]