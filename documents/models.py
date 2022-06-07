from datetime import datetime
import time

from polymorphic.models import PolymorphicModel
from django.db import models

from accounts.models import Profile


def get_attachment_directory_path(instance, filename):
    return '%d/%d/%s' % (int(datetime.now().year), int(datetime.now().month), filename)


class DocumentAttachment(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=get_attachment_directory_path, max_length=255)
    description = models.TextField(null=True, blank=True)


DOCUMENT_TYPES = [
    ('Article', 'مقاله'),
    ('Resume', 'رزومه'),
    ('Book', 'کتاب'),
    ('Experience', 'تجربه'),
    ('Thesis', 'پایان نامه'),
    ('Idea', 'ایده'),
    ('Seminar', 'سمینار'),
    ('Workshop', 'کارگاه'),
    ('Conference', 'کنفرانس'),
    ('Visit', 'بازدید'),
    ('Project', 'پروژه'),
    ('Manual', 'دستورالعمل'),
    ('Report', 'گزارش'),
    ('Journal', 'فصلنامه'),
    ('Future', 'آینده پژوهی'),
    ('CoWork', 'همکاری'),
]


DOCUMENT_FIELDS = [
    ('field-1', 'حوزه نمونه ۱'),
    ('field-2', 'حوزه نمونه ۲'),
    ('field-3', 'حوزه نمونه ۳'),
    ('No Field', 'بدون حوزه'),
]


CENTER_LIST = [
    ('center-11', 'م.حاجت زاه(شناوری)'),
    ('center-12', 'م.تهرانی(سلاح و مهمات)'),
    ('center-13', 'ش.رضایی(موشکی)'),
    ('center-14', 'ش.محمدیها(هوادریا)'),
    ('center-15', 'ش.چمران(الکترونیک)'),
    ('center-16', 'ش.همدانی(پدافند)'),
    ('center-17', 'م.جلالی(مواد)'),
    ('center-18', 'ش.مهدوی(فناوری)'),
    ('center-19', 'مد.نوآوری(مد.دانش-آینده پژوهی)'),
    ('center-20', 'مد.تحقیقات(تحقیقات)'),
    ('center-21', 'ش.ناظری(موتور)'),
    ('center-22', 'زیرسطحی'),
    ('center-23', 'ش.آبسالان(فیزیک دریا)'),
    ('center-24', 'ش.عسگری(رادار)'),
    ('center-25', 'بازرسی-بهداری'),
]


class Document(PolymorphicModel):
    title = models.CharField(max_length=255)
    organization_code = models.CharField(max_length=255)
    center = models.CharField(max_length=255, choices=CENTER_LIST)
    field = models.CharField(max_length=255, choices=DOCUMENT_FIELDS)
    type = models.CharField(max_length=255, choices=DOCUMENT_TYPES)
    description = models.TextField(null=True, blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    attachments = models.ManyToManyField(DocumentAttachment, blank=True, related_name='attachments')

    @property
    def organization_code_counter(self):
        return int(self.organization_code.split('-')[2][2:])

    @property
    def organization_code_year(self):
        return self.organization_code.split('-')[1]


class Resume(Document):
    profile = models.OneToOneField(to=Profile, on_delete=models.CASCADE)
    entrance_year = models.IntegerField()
    measure = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)


ARTICLE_PUBLISH_TYPES = [
    ('Paper', 'مجله'),
    ('Conference', 'کنفرانس'),
]

ARTICLE_PUBLISH_LEVELS = [
    #magazine
    ('ISI', 'ISI'),
    ('ISC', 'ISC'),
    ('Research', 'علمی-پژوهشی'),
    ('Extension', 'علمی-ترویجی'),
    ('Specialized', 'علمی-تخصصی'),
    #conference
    ('Departmental', 'داخلی'),
    ('National', 'ملی'),
    ('International', 'بین المللی'),
]

ARTICLE_CONFERENCE_PUBLISH_LEVELS = [
    ('Departmental', 'داخلی'),
    ('National', 'ملی'),
    ('International', 'بین المللی'),
]

ARTICLE_MAGANIZE_PUBLISH_LEVELS = [
    ('ISI', 'ISI'),
    ('ISC', 'ISC'),
    ('Research', 'علمی-پژوهشی'),
    ('Extension', 'علمی-ترویجی'),
    ('Specialized', 'علمی-تخصصی'),
]


class Article(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='article_producer')
    key_words = models.TextField()
    published_at = models.DateTimeField()
    publish_type = models.CharField(max_length=255, choices=ARTICLE_PUBLISH_TYPES)
    publish_level = models.CharField(max_length=255, choices=ARTICLE_PUBLISH_LEVELS)
    publish_title = models.CharField(max_length=255)


class Experience(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='experience_producer')
    judges = models.TextField()
    presented_at = models.DateTimeField()
    assessment_result = models.CharField(max_length=255)


class Book(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='book_producer')
    fipa = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    publisher = models.CharField(max_length=255)
    judges=models.TextField()
    assessment_result = models.CharField(max_length=255)


class Idea(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='idea_producer')
    judges = models.TextField()
    presented_at = models.DateTimeField()
    assessment_result = models.CharField(max_length=255)


class Seminar(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='seminar_producer')
    judges = models.TextField()
    presented_at = models.DateTimeField()
    participant_number = models.IntegerField()
    assessment_result = models.CharField(max_length=255)


WORKSHOP_TYPES = [
    ('Technical', 'کارگاه فنی'),
    ('Scientific', 'کارگاه علمی'),
    ('Course', 'دوره آموزشی'),
]


class Workshop(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='workshop_producer')
    started_at = models.DateTimeField()
    meeting_number = models.IntegerField()
    participant_number = models.IntegerField()
    location = models.CharField(max_length=255)
    workshop_type = models.CharField(max_length=255, choices=WORKSHOP_TYPES)


CONFERENCE_LEVELS=[
    ('Citywid', 'شهری'),
    ('Regional', 'استانی'),
    ('Countrywide', 'کشوری'),
    ('Wordwide', 'بین المللی'),
]


class Conference(Document):
    held_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    conference_level = models.CharField(max_length=255, choices=CONFERENCE_LEVELS)


class Visit(Document):
    location = models.CharField(max_length=255)
    visited_at = models.DateTimeField()
    participant_number = models.IntegerField()


class Manual(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='manual_producer')
    declared_at = models.DateTimeField()


class Project(Document):
    finished_at = models.DateTimeField()
    manager = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='project_manager')


class Report(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='report_producer')
    presented_at = models.DateTimeField()
    related_project = models.ForeignKey(to=Project, on_delete=models.PROTECT, related_name='report_project')


class Thesis(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='thesis_producer')
    presented_at = models.DateTimeField()
    university = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)


class Journal(Document):
    presented_at = models.DateTimeField()
    page_number = models.IntegerField()


FUTURE_TYPES = [
    ('Rasadi', 'گزارش رصدی'),
    ('Info', 'اینفوگرافی'),
    ('Dide', 'دیده بان'),
    ('Organ', 'گزارش سازمانی'),
]


class Future(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='future_producer')
    presented_at = models.DateTimeField()
    future_type = models.CharField(max_length=255, choices=FUTURE_TYPES)



COWORK_TYPES = [
    ('Company', 'شرکت'),
    ('University', 'دانشگاه'),
]


PERSON_TYPES = [
    ('Real', 'حقیقی'),
    ('Legal', 'حقوقی'),
]


class CoWork(Document):
    person_type = models.CharField(max_length=255, choices=PERSON_TYPES)
    cowork_type = models.CharField(max_length=255, choices=COWORK_TYPES)
    address = models.TextField()


class CenterData(PolymorphicModel):
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    organization_code = models.CharField(max_length=255)
    center = models.CharField(max_length=255, choices=CENTER_LIST)
    field = models.CharField(max_length=255, choices=DOCUMENT_FIELDS)
    type = models.CharField(max_length=255, choices=DOCUMENT_TYPES)

    description = models.TextField(null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    attachments = models.ManyToManyField(DocumentAttachment, blank=True, related_name='attachments')

