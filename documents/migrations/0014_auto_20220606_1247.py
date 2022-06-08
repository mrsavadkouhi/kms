# Generated by Django 2.2.13 on 2022-06-06 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0013_auto_20220606_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publish_title',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_level',
            field=models.CharField(choices=[('ISI', 'ISI'), ('ISC', 'ISC'), ('Research', 'علمی-پژوهشی'), ('Extension', 'علمی-ترویجی'), ('Specialized', 'علمی-تخصصی'), ('Departmental', 'داخلی'), ('National', 'ملی'), ('International', 'بین المللی')], max_length=255),
        ),
    ]