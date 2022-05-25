from datetime import datetime
import time

from polymorphic.models import PolymorphicModel
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile

STATUS_TYPES = [
    ('to_do', 'جهت انجام'),
    ('inprogress', 'در حال انجام'),
    ('completed', 'انجام شده'),
    ('verified', 'تایید شده'),
]

TRANSACTION_TITTLES = [
    ('prepayment', 'پیش پرداخت'),
    ('installment', 'قسط'),
    ('paragraph', 'بند'),
]


def get_attachment_directory_path(instance, filename):
    return '%s/%d/%d/%s' % (instance.attachments.first().type, int(datetime.now().year), int(datetime.now().month), filename)


class DocumentAttachment(models.Model):
    file = models.FileField(upload_to=get_attachment_directory_path, max_length=255)
    description = models.TextField(null=True, blank=True)


class Document(PolymorphicModel):
    TYPES = [
        ('Article', 'مقاله'),
    ]

    title = models.CharField(max_length=255)
    organization_code = models.CharField(max_length=255)
    center = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=TYPES)

    attachments = models.ManyToManyField(DocumentAttachment, blank=True, related_name='attachments')


class Resume(Document):
    military_code = models.CharField(max_length=255)
    entrance_year = models.IntegerField()
    measure = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)


class Article(Document):
    PUBLISH_TYPES = [
        ('Article', 'مقاله'),
    ]
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='article_producer')
    key_words = models.TextField()
    published_at = models.DateTimeField()
    publish_type = models.CharField(max_length=255, choices=PUBLISH_TYPES)


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
    participants_number = models.IntegerField()
    assessment_result = models.CharField(max_length=255)


class Workshop(Document):
    WORKSHOP_TYPES=[
        ('Article', 'مقاله'),
    ]
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='workshop_producer')
    judges = models.TextField()
    started_at = models.DateTimeField()
    meeting_number = models.IntegerField()
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=WORKSHOP_TYPES)


class Conference(Document):
    CONFERENCE_LEVELS=[
        ('Article', 'مقاله'),
    ]
    held_at = models.DateTimeField()
    location = models.CharField(max_length=255)
    level = models.CharField(max_length=255, choices=CONFERENCE_LEVELS)


class Visit(Document):
    location = models.CharField(max_length=255)
    visited_at = models.DateTimeField()
    participant_number = models.IntegerField()


class Manual(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='manual_producer')
    declared_at = models.DateTimeField()


class Report(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='report_producer')
    presented_at = models.DateTimeField()
    related_project = models.CharField(max_length=255)


class Projects(Document):
    finished_at = models.DateTimeField()
    manager = models.CharField(max_length=255)
    description = models.TextField()


class Thesis(Document):
    university = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)


class Journal(Document):
    presented_at = models.DateTimeField()
    page_number = models.IntegerField()


class Future(Document):
    FUTURE_TYPES = [
        ('Article', 'مقاله'),
    ]

    presented_at = models.DateTimeField()
    type = models.CharField(max_length=255, choices=FUTURE_TYPES)


class CoWork(Document):
    COWORK_TYPES = [
        ('Company', 'شرکت'),
        ('University', 'دانشگاه'),
    ]
    PERSON_TYPES = [
        ('Real', 'حقیقی'),
        ('Legal', 'حقوقی'),
    ]

    address = models.TextField()
    description = models.TextField()

