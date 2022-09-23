from datetime import datetime
import time

from polymorphic.models import PolymorphicModel
from django.db import models

from accounts.models import Profile


def get_attachment_directory_path(instance, filename):
    return '%d/%d/%s' % (int(datetime.now().year), int(datetime.now().month), filename)


def get_avatar_directory_path(instance, filename):
    return 'resumes/%d_avatar_%s' % (int(time.time()), filename)


def get_center_avatar_directory_path(instance, filename):
    return 'centers/%d_avatar_%s' % (int(time.time()), filename)


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
    ('Order', 'حکم'),
    ('Invention', 'ثبت اختراع'),
    ('Assessment', 'ارزیابی'),
]


# CENTER_LIST = [
#     ('center-11', 'م.حاجت زاه(شناوری)'),
#     ('center-12', 'م.تهرانی(سلاح و مهمات)'),
#     ('center-13', 'ش.رضایی(موشکی)'),
#     ('center-14', 'ش.محمدیها(هوادریا)'),
#     ('center-15', 'ش.چمران(الکترونیک)'),
#     ('center-16', 'ش.همدانی(پدافند)'),
#     ('center-17', 'م.جلالی(مواد)'),
#     ('center-18', 'ش.مهدوی(فناوری)'),
#     ('center-19', 'مد.نوآوری(مد.دانش-آینده پژوهی)'),
#     ('center-20', 'مد.تحقیقات(تحقیقات)'),
#     ('center-21', 'ش.ناظری(موتور)'),
#     ('center-22', 'زیرسطحی'),
#     ('center-23', 'ش.آبسالان(فیزیک دریا)'),
#     ('center-24', 'ش.عسگری(رادار)'),
#     ('center-25', 'بازرسی-بهداری'),
# ]


class Center(models.Model):
    avatar=models.ImageField(upload_to=get_center_avatar_directory_path, max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, unique=True)
    code = models.IntegerField()


class Document(PolymorphicModel):
    title = models.CharField(max_length=255, null=True, blank=True)
    organization_code = models.CharField(max_length=255, null=True, blank=True)
    center = models.ForeignKey(to=Center, on_delete=models.PROTECT, related_name='center', null=True, blank=True)
    field = models.CharField(max_length=255,null=True, blank=True)
    type = models.CharField(max_length=255, choices=DOCUMENT_TYPES)
    description = models.TextField(null=True, blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    attachments = models.ManyToManyField(DocumentAttachment, blank=True, related_name='attachments')

    @property
    def organization_code_counter(self):
        try:
            return int(self.organization_code.split('-')[2][2:])
        except:
            return None

    @property
    def organization_code_year(self):
        try:
            return self.organization_code.split('-')[1]
        except:
            return None


class Resume(Document):
    # profile = models.OneToOneField(to=Profile, on_delete=models.CASCADE)
    avatar=models.ImageField(upload_to=get_avatar_directory_path, max_length=255, blank=True, null=True)
    entrance_year = models.IntegerField(null=True, blank=True)
    measure = models.CharField(max_length=255,null=True, blank=True)
    degree = models.CharField(max_length=255,null=True, blank=True)


VERIFICATION_TYPES = [
    ('verified', 'تایید شد'),
    ('not-verified', 'تایید نشد'),
]

class Order(Document):
    receiver = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='order_receiver')
    issued_at = models.DateTimeField()
    sent_at = models.DateTimeField()
    answered_at = models.DateTimeField()
    owner = models.CharField(max_length=255)
    verification = models.CharField(max_length=255, choices=VERIFICATION_TYPES)
    other = models.CharField(max_length=255, null=True, blank=True)


class Invention(Document):
    producers = models.ManyToManyField(to=Resume, related_name='invention_producers')
    registered_at = models.DateTimeField()
    project_title = models.CharField(max_length=255)


class Assessment(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='assessment_resume')
    elite_received_at = models.DateTimeField()
    order_issued_at = models.DateTimeField()
    issue_code = models.CharField(max_length=255)
    scientific_rank = models.CharField(max_length=255)
    father = models.CharField(max_length=255)
    profile_type = models.CharField(max_length=255)
    necessary_condition = models.TextField(null=True, blank=True)
    sufficient_condition = models.TextField(null=True, blank=True)


ARTICLE_PUBLISH_TYPES = [
    ('Paper', 'مجله'),
    ('Conference', 'کنفرانس'),
]

ARTICLE_PUBLISH_LEVELS = [
    #magazine
    ('ISI', 'ISI'),
    ('ISC', 'ISC'),
    ('Journal', 'فصلنامه'),
    ('Research', 'علمی-پژوهشی'),
    ('Extension', 'علمی-ترویجی'),
    ('Specialized', 'علمی-تخصصی'),
    #conference
    ('Sepah', 'سپاه'),
    ('Martial', 'نیروهای مسلح'),
    ('National', 'ملی'),
    ('International', 'بین المللی'),
]

ARTICLE_CONFERENCE_PUBLISH_LEVELS = [
    ('Sepah', 'سپاه'),
    ('Martial', 'نیروهای مسلح'),
    ('National', 'ملی'),
    ('International', 'بین المللی'),
]

ARTICLE_MAGANIZE_PUBLISH_LEVELS = [
    ('ISI', 'ISI'),
    ('ISC', 'ISC'),
    ('Journal', 'فصلنامه'),
    ('Research', 'علمی-پژوهشی'),
    ('Extension', 'علمی-ترویجی'),
    ('Specialized', 'علمی-تخصصی'),
]


class Article(Document):
    producers = models.ManyToManyField(to=Resume, related_name='article_producers')
    judges = models.ManyToManyField(to=Resume, related_name='article_judges', blank=True, null=True)
    key_words = models.TextField(blank=True, null=True)
    published_at = models.DateTimeField()
    publish_type = models.CharField(max_length=255, choices=ARTICLE_PUBLISH_TYPES)
    publish_level = models.CharField(max_length=255, choices=ARTICLE_PUBLISH_LEVELS)
    publish_title = models.CharField(max_length=255)


class Experience(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='experience_producer')
    judges=models.ManyToManyField(to=Resume, related_name='experience_judges', blank=True, null=True)
    presented_at = models.DateTimeField()
    assessment_result = models.CharField(max_length=255)


class Book(Document):
    producers=models.ManyToManyField(to=Resume, related_name='book_producers')
    fipa = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    publisher = models.CharField(max_length=255)
    judges=models.ManyToManyField(to=Resume, related_name='book_judges', blank=True, null=True)
    assessment_result = models.CharField(max_length=255)


class Idea(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='idea_producer')
    judges=models.ManyToManyField(to=Resume, related_name='idea_judges', blank=True, null=True)
    presented_at = models.DateTimeField()
    assessment_result = models.CharField(max_length=255)


class Seminar(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='seminar_producer')
    judges=models.ManyToManyField(to=Resume, related_name='seminar_judges', blank=True, null=True)
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
    duration = models.IntegerField()
    finished_at = models.DateTimeField()
    manager = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='project_manager')
    middle_attachments = models.ManyToManyField(DocumentAttachment, blank=True, related_name='middle_project_attachments')
    end_attachments = models.ManyToManyField(DocumentAttachment, blank=True, related_name='end_project_attachments')


class Report(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='report_producer')
    presented_at = models.DateTimeField()
    related_project=models.CharField(max_length=255)


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
    ('Other', 'سایر'),
]


class Future(Document):
    producer = models.ForeignKey(to=Resume, on_delete=models.PROTECT, related_name='future_producer')
    presented_at = models.DateTimeField()
    other = models.CharField(max_length=255, null=True, blank=True)
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
    address = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField()


class CenterPersonnel(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    national_code = models.CharField(max_length=255)
    birth_year=models.IntegerField()
    measure=models.CharField(max_length=255)
    sub_measure=models.CharField(max_length=255)
    degree=models.CharField(max_length=255)
    university=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    address=models.TextField(max_length=255)
    phone=models.CharField(max_length=255)
    mobile=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    basij_entrance_year=models.IntegerField()
    basij_city=models.CharField(max_length=255)
    pre_empowerment = models.CharField(max_length=255)
    com_empowerment = models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)


CENTERPROJECT_LEVELS = [
    ('predev', 'پیش رشد'),
    ('first', 'سطح یک'),
    ('second', 'سطح دو'),
    ('third', 'سطح سه'),
]


class CenterProject(models.Model):
    contract_number = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    level = models.CharField(max_length=255, choices=CENTERPROJECT_LEVELS)
    status = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)


CENTERDATA_TYPES = [
    ('Core', 'هسته'),
    ('TechUnit', 'واحد فناورانه'),
    ('Comapny', 'شرکت'),
]


class CenterData(PolymorphicModel):
    type = models.CharField(max_length=255, choices=CENTERDATA_TYPES)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    manager = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    establish_year = models.IntegerField()
    number = models.IntegerField()
    activity_field = models.CharField(max_length=255)
    professional_field = models.CharField(max_length=255)

    personnels = models.ManyToManyField(CenterPersonnel, blank=True, related_name='personnel')
    projects = models.ManyToManyField(CenterProject, blank=True, related_name='projects')

    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    attachments = models.ManyToManyField(DocumentAttachment, blank=True, related_name='center_attachments')

    @property
    def pre_dev_level(self):
        return self.projects.filter(level='predev').count()

    @property
    def first_level(self):
        return self.projects.filter(level='first').count()

    @property
    def second_level(self):
        return self.projects.filter(level='second').count()

    @property
    def third_level(self):
        return self.projects.filter(level='third').count()


class Core(CenterData):
    pass


class Tech(CenterData):
    pass


class Company(CenterData):
    pass
