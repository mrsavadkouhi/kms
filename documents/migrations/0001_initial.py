# Generated by Django 2.2.13 on 2022-06-26 14:14

from django.db import migrations, models
import django.db.models.deletion
import documents.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='CenterData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Core', 'هسته'), ('TechUnit', 'واحد فناورانه'), ('Comapny', 'شرکت')], max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('manager', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=255)),
                ('establish_year', models.IntegerField()),
                ('number', models.IntegerField()),
                ('activity_field', models.CharField(max_length=255)),
                ('professional_field', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='CenterPersonnel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('national_code', models.CharField(max_length=255)),
                ('birth_year', models.IntegerField()),
                ('measure', models.CharField(max_length=255)),
                ('sub_measure', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=255)),
                ('university', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('address', models.TextField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('basij_entrance_year', models.IntegerField()),
                ('basij_city', models.CharField(max_length=255)),
                ('pre_empowerment', models.CharField(max_length=255)),
                ('com_empowerment', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CenterProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('predev', 'پیش رشد'), ('first', 'سطح یک'), ('second', 'سطح دو'), ('third', 'سطح سه')], max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('organization_code', models.CharField(blank=True, max_length=255, null=True)),
                ('field', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(choices=[('Article', 'مقاله'), ('Resume', 'رزومه'), ('Book', 'کتاب'), ('Experience', 'تجربه'), ('Thesis', 'پایان نامه'), ('Idea', 'ایده'), ('Seminar', 'سمینار'), ('Workshop', 'کارگاه'), ('Conference', 'کنفرانس'), ('Visit', 'بازدید'), ('Project', 'پروژه'), ('Manual', 'دستورالعمل'), ('Report', 'گزارش'), ('Journal', 'فصلنامه'), ('Future', 'آینده پژوهی'), ('CoWork', 'همکاری'), ('Order', 'حکم'), ('Invention', 'ثبت اختراع'), ('Assessment', 'ارزیابی')], max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='DocumentAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(max_length=255, upload_to=documents.models.get_attachment_directory_path)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('centerdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.CenterData')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.centerdata',),
        ),
        migrations.CreateModel(
            name='Conference',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('held_at', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('conference_level', models.CharField(choices=[('Citywid', 'شهری'), ('Regional', 'استانی'), ('Countrywide', 'کشوری'), ('Wordwide', 'بین المللی')], max_length=255)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Core',
            fields=[
                ('centerdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.CenterData')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.centerdata',),
        ),
        migrations.CreateModel(
            name='CoWork',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('person_type', models.CharField(choices=[('Real', 'حقیقی'), ('Legal', 'حقوقی')], max_length=255)),
                ('cowork_type', models.CharField(choices=[('Company', 'شرکت'), ('University', 'دانشگاه')], max_length=255)),
                ('address', models.TextField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('presented_at', models.DateTimeField()),
                ('page_number', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('entrance_year', models.IntegerField()),
                ('measure', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=255)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Tech',
            fields=[
                ('centerdata_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.CenterData')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.centerdata',),
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('location', models.CharField(max_length=255)),
                ('visited_at', models.DateTimeField()),
                ('participant_number', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.AddField(
            model_name='document',
            name='attachments',
            field=models.ManyToManyField(blank=True, related_name='attachments', to='documents.DocumentAttachment'),
        ),
        migrations.AddField(
            model_name='document',
            name='center',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='center', to='documents.Center'),
        ),
        migrations.AddField(
            model_name='document',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_documents.document_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='centerdata',
            name='attachments',
            field=models.ManyToManyField(blank=True, related_name='center_attachments', to='documents.DocumentAttachment'),
        ),
        migrations.AddField(
            model_name='centerdata',
            name='personnels',
            field=models.ManyToManyField(blank=True, related_name='personnel', to='documents.CenterPersonnel'),
        ),
        migrations.AddField(
            model_name='centerdata',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_documents.centerdata_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='centerdata',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='projects', to='documents.CenterProject'),
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('started_at', models.DateTimeField()),
                ('meeting_number', models.IntegerField()),
                ('participant_number', models.IntegerField()),
                ('location', models.CharField(max_length=255)),
                ('workshop_type', models.CharField(choices=[('Technical', 'کارگاه فنی'), ('Scientific', 'کارگاه علمی'), ('Course', 'دوره آموزشی')], max_length=255)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='workshop_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Thesis',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('presented_at', models.DateTimeField()),
                ('university', models.CharField(max_length=255)),
                ('measure', models.CharField(max_length=255)),
                ('degree', models.CharField(max_length=255)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='thesis_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Seminar',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('presented_at', models.DateTimeField()),
                ('participant_number', models.IntegerField()),
                ('assessment_result', models.CharField(max_length=255)),
                ('judges', models.ManyToManyField(related_name='seminar_judges', to='documents.Resume')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='seminar_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('presented_at', models.DateTimeField()),
                ('related_project', models.CharField(max_length=255)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='report_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('duration', models.IntegerField()),
                ('finished_at', models.DateTimeField()),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project_manager', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('issued_at', models.DateTimeField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_receiver', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Manual',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('declared_at', models.DateTimeField()),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='manual_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Invention',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('registered_at', models.DateTimeField()),
                ('project_title', models.CharField(max_length=255)),
                ('producers', models.ManyToManyField(related_name='invention_producers', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('presented_at', models.DateTimeField()),
                ('assessment_result', models.CharField(max_length=255)),
                ('judges', models.ManyToManyField(related_name='idea_judges', to='documents.Resume')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='idea_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Future',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('presented_at', models.DateTimeField()),
                ('future_type', models.CharField(choices=[('Rasadi', 'گزارش رصدی'), ('Info', 'اینفوگرافی'), ('Dide', 'دیده بان'), ('Organ', 'گزارش سازمانی')], max_length=255)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='future_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('presented_at', models.DateTimeField()),
                ('assessment_result', models.CharField(max_length=255)),
                ('judges', models.ManyToManyField(related_name='experience_judges', to='documents.Resume')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='experience_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('fipa', models.CharField(max_length=255)),
                ('published_at', models.DateTimeField()),
                ('publisher', models.CharField(max_length=255)),
                ('assessment_result', models.CharField(max_length=255)),
                ('judges', models.ManyToManyField(related_name='book_judges', to='documents.Resume')),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='book_producer', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('elite_received_at', models.DateTimeField()),
                ('order_issued_at', models.DateTimeField()),
                ('issue_code', models.CharField(max_length=255)),
                ('scientific_rank', models.CharField(max_length=255)),
                ('father', models.CharField(max_length=255)),
                ('profile_type', models.CharField(max_length=255)),
                ('necessary_condition', models.TextField()),
                ('sufficient_condition', models.TextField()),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='assessment_resume', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='documents.Document')),
                ('key_words', models.TextField()),
                ('published_at', models.DateTimeField()),
                ('publish_type', models.CharField(choices=[('Paper', 'مجله'), ('Conference', 'کنفرانس')], max_length=255)),
                ('publish_level', models.CharField(choices=[('ISI', 'ISI'), ('ISC', 'ISC'), ('Research', 'علمی-پژوهشی'), ('Extension', 'علمی-ترویجی'), ('Specialized', 'علمی-تخصصی'), ('Sepah', 'سپاه'), ('Martial', 'نیروهای مسلح'), ('National', 'ملی'), ('International', 'بین المللی')], max_length=255)),
                ('publish_title', models.CharField(max_length=255)),
                ('judges', models.ManyToManyField(related_name='article_judges', to='documents.Resume')),
                ('producers', models.ManyToManyField(related_name='article_producers', to='documents.Resume')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('documents.document',),
        ),
    ]
