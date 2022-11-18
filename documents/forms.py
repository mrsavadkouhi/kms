import jdatetime
import openpyxl
import pandas as pd
from django import forms
from django.core.exceptions import ValidationError

from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm


class DocumentAttachmentForm(BSModalModelForm):
    document_id = forms.IntegerField(required=True)
    project_doc_type = forms.CharField(required=False)
    file = forms.FileField(required=True)
    description = forms.CharField(required=False)

    class Meta:
        model = DocumentAttachment
        fields = ['file', 'description']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        document = Document.objects.get(id=self.cleaned_data['document_id'])
        project_doc_type = self.cleaned_data['project_doc_type']
        if project_doc_type == 'Middle':
            document.middle_attachments.add(instance)
        elif project_doc_type == 'End':
            document.end_attachments.add(instance)
        else:
            document.attachments.add(instance)

        return self.instance


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class InventionForm(forms.ModelForm):
    class Meta:
        model = Invention
        fields = '__all__'


class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = '__all__'


class CenterForm(forms.ModelForm):
    class Meta:
        model = Center
        fields = '__all__'


class ResumeForm(forms.ModelForm):
    title = forms.CharField(required=True)
    class Meta:
        model = Resume
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')
        if title:
            if Resume.objects.filter(title=title).exists():
                raise forms.ValidationError("نام و نام خانوادگی از قبل وجود داشته است.")

        return cleaned_data


class ResumeEditForm(forms.ModelForm):
    title = forms.CharField(required=True)
    class Meta:
        model = Resume
        fields = '__all__'


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = '__all__'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = '__all__'


class SeminarForm(forms.ModelForm):
    class Meta:
        model = Seminar
        fields = '__all__'


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = '__all__'


class ConferenceForm(forms.ModelForm):
    class Meta:
        model = Conference
        fields = '__all__'


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = '__all__'


class ManualForm(forms.ModelForm):
    class Meta:
        model = Manual
        fields = '__all__'


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = '__all__'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class ThesisForm(forms.ModelForm):
    class Meta:
        model = Thesis
        fields = '__all__'


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = '__all__'


class FutureForm(forms.ModelForm):
    class Meta:
        model = Future
        fields = '__all__'


class CoWorkForm(forms.ModelForm):
    class Meta:
        model = CoWork
        fields = '__all__'


class CoreForm(forms.ModelForm):
    class Meta:
        model = Core
        fields = '__all__'


class TechForm(forms.ModelForm):
    class Meta:
        model = Tech
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class CenterPersonnelForm(forms.ModelForm):
    document_id = forms.IntegerField(required=True)

    class Meta:
        model = CenterPersonnel
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        document = CenterData.objects.get(id=self.cleaned_data['document_id'])
        document.personnels.add(instance)
        return self.instance


class CenterProjectForm(forms.ModelForm):
    document_id = forms.IntegerField(required=True)

    class Meta:
        model = CenterProject
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        document = CenterData.objects.get(id=self.cleaned_data['document_id'])
        document.projects.add(instance)
        return self.instance


class CenterAttachmentForm(BSModalModelForm):
    document_id = forms.IntegerField(required=True)
    file = forms.FileField(required=True)
    description = forms.CharField(required=False)

    class Meta:
        model = DocumentAttachment
        fields = ['file', 'description']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        document = CenterData.objects.get(id=self.cleaned_data['document_id'])
        document.attachments.add(instance)
        return self.instance


class DocumentImportForm(forms.Form):
    excel_file = forms.FileField()
    doc_type = forms.CharField()

    def check_organization_code(self, type, code):
        years = ['pre98', '98', '99']
        for i in range(400, 430):
            years.append(str(i))

        try:
            code_sections = code.split('-')
            if len(code_sections) != 3:
                return False
            elif code_sections[0] != 'KM/'+type:
                return False
            elif code_sections[1] not in years:
                return False
            elif len(code_sections[2]) < 3:
                return False
            temp = int(code_sections[2])
        except:
            return False
        return True

    def check_articles(self, excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('P',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            published_at = row[5]
            if published_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ چاپ در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()
            except:
                raise forms.ValidationError("فرمت اطلاعات ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            publish_title = row[8]

            center = row[9]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[4] in ['nan', None, '']:
                raise forms.ValidationError("ستون نویسندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[4].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون نویسندگان در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            publish_type = row[6]
            if publish_type in ['nan', None, 'None', '']:
               publish_type = None
            else:
                flag = True
                for name, des in ARTICLE_PUBLISH_TYPES:
                    if publish_type == des:
                        publish_type = name
                        flag = False
                if flag:
                    raise forms.ValidationError(
                        "فرمت اطلاعات ستون نوع انتشار در خط " + str(error_line) + " فایل صحیح نیست")

            publish_level = row[7]
            if publish_level in ['nan', None, 'None', '']:
               publish_level = None
            else:
                flag = True
                for name, des in ARTICLE_PUBLISH_LEVELS:
                    if publish_level == des:
                        publish_level=name
                        flag = False
                if flag:
                    raise forms.ValidationError(
                        "فرمت اطلاعات ستون سطح انتشار در خط " + str(error_line) + " فایل صحیح نیست")

            field = row[2]
            doc_type = 'Article'
            key_words = row[3]

            cleaned_data.append((title, organization_code, doc_type, field, key_words, producers_list, published_at, publish_title, publish_type, publish_level, center))
        return cleaned_data

    def import_articles(self, excel_data):
        cleaned_data = self.check_articles(excel_data)
        for title, organization_code, doc_type, field, key_words, producers_list, published_at, publish_title, publish_type, publish_level, center in cleaned_data:
            article = Article.objects.create(
                title=title,
                organization_code=organization_code,
                field=field,
                type=doc_type,
                key_words=key_words,
                published_at=published_at,
                publish_level=publish_level,
                publish_type=publish_type,
                publish_title=publish_title,
                center=center,
            )

            article.producers.set(producers_list)

    def check_books(self, excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('B',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            published_at = row[6]
            if published_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ چاپ در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()
            except:
                raise forms.ValidationError("فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            publisher = row[5]

            # assessment_result = row[8]
            # if assessment_result in ['nan', None, '']:
            #     raise forms.ValidationError("ستون ارزشیابی در خط " + str(error_line) + " نمی تواند خالی باشد.")

            fipa = row[4]
            if fipa in ['nan', None, '']:
                raise forms.ValidationError("ستون فیپا در خط " + str(error_line) + " نمی تواند خالی باشد.")

            center = row[8]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون نویسندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون نویسندگان در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            field = row[2]
            assessment_result = row[7]
            doc_type = 'Book'

            cleaned_data.append((title, organization_code, doc_type, field, assessment_result, producers_list, published_at, publisher, fipa, center))
        return cleaned_data

    def import_books(self,excel_data):
        cleaned_data = self.check_books(excel_data)
        for title, organization_code, doc_type, field, assessment_result, producers_list, published_at, publisher, fipa, center in cleaned_data:
            book = Book.objects.create(
                title=title,
                field=field,
                assessment_result=assessment_result,
                organization_code=organization_code,
                type=doc_type,
                publisher=publisher,
                fipa=fipa,
                published_at=published_at,
                center=center,
                                   )
            book.producers.set(producers_list)

    def check_experiences(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('E',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            presented_at=row[4]
            if presented_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ ارائه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
            except:
                raise forms.ValidationError("فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            center=row[6]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون تجربه نگاران در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون تجربه نگاران در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            field = row[2]
            assessment_result = row[5]
            doc_type='Experience'
            
            cleaned_data.append((title, organization_code, doc_type, field, assessment_result, producers_list, presented_at, center))
        return cleaned_data

    def import_experiences(self,excel_data):
        cleaned_data = self.check_experiences(excel_data)
        for title, organization_code, doc_type, field, assessment_result, producers_list, presented_at, center in cleaned_data:
            experience=Experience.objects.create(
                title=title,
                field=field,
                organization_code=organization_code,
                type=doc_type,
                presented_at=presented_at,
                assessment_result=assessment_result,
                center=center,
            )
            experience.producers.set(producers_list)

    def check_ideas(self,excel_data):
        error_line=1
        cleaned_data=[]
        for row in excel_data:
            error_line+=1

            title=row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code=row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('I',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            presented_at=row[4]
            if presented_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ ارائه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
            except:
                raise forms.ValidationError("فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            center=row[6]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center=Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون ایده پردازان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون ایده پردازان در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            field = row[2]
            assessment_result = row[5]
            doc_type='Idea'

            cleaned_data.append((title, organization_code, doc_type,field, assessment_result, producers_list, presented_at, center))
        return cleaned_data

    def import_ideas(self,excel_data):
        cleaned_data = self.check_ideas(excel_data)
        for title, organization_code, doc_type,field, assessment_result, producers_list, presented_at, center in cleaned_data:
            idea=Idea.objects.create(
                title=title,
                field=field,
                assessment_result=assessment_result,
                organization_code=organization_code,
                type=doc_type,
                presented_at=presented_at,
                center=center,
            )
            idea.producers.set(producers_list)

    def check_theses(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('T',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            measure=row[4]
            if measure in ['nan', None, '']:
                raise forms.ValidationError("ستون رشته تحصیلی در خط " + str(error_line) + " نمی تواند خالی باشد.")

            degree=row[5]
            if degree in ['nan', None, '']:
                raise forms.ValidationError("ستون مقطع تحصیلی در خط " + str(error_line) + " نمی تواند خالی باشد.")

            university=row[6]
            if university in ['nan', None, '']:
                raise forms.ValidationError("ستون دانشگاه در خط " + str(error_line) + " نمی تواند خالی باشد.")

            presented_at=row[7]
            if presented_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ دفاع در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
            except:
                raise forms.ValidationError("فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            center=row[8]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            producer=row[3]
            if producer in ['nan', None, '']:
                raise forms.ValidationError("ستون دانشجو در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون دانشجو در خط " + str(error_line) + " فایل صحیح نیست")

            field = row[2]
            doc_type='Thesis'

            cleaned_data.append((title,field, organization_code, doc_type, producer_obj, presented_at, measure, degree, university, center))
        return cleaned_data

    def import_theses(self, excel_data):
        cleaned_data = self.check_theses(excel_data)
        for title,field, organization_code, doc_type, producer_obj, presented_at, measure, degree, university, center in cleaned_data:
            thesis=Thesis.objects.create(
                title=title,
                field=field,
                organization_code=organization_code,
                type=doc_type,
                producer=producer_obj,
                presented_at=presented_at,
                measure=measure,
                degree=degree,
                university=university,
                center=center,
            )

    def check_manuals(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('M',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            declared_at=row[4]
            if declared_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ ابلاغ در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                declared_at=jdatetime.datetime.strptime(declared_at, "%Y/%m/%d")
                declared_at=declared_at.togregorian()
            except:
                raise forms.ValidationError("فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            center=row[5]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون تهیه کنندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون تهیه کنندگان در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            field=row[2]
            doc_type='Manual'

            cleaned_data.append((title, organization_code, doc_type, field, producers_list, declared_at, center))
        return cleaned_data

    def import_manuals(self,excel_data):
        cleaned_data = self.check_manuals(excel_data)
        for title, organization_code, doc_type, field, producers_list, declared_at, center in cleaned_data:
            manual=Manual.objects.create(
                title=title,
                organization_code=organization_code,
                field=field,
                type=doc_type,
                declared_at=declared_at,
                center=center,
            )
            manual.producers.set(producers_list)

    def check_orders(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            # organization_code = row[1]
            # if organization_code in ['nan', None, '']:
            #     raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")

            owner = row[2]

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون داوری در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون داوری در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            issued_at=row[4]
            if issued_at in ['nan', None, 'None', '']:
                issued_at = None
            else:
                try:
                    issued_at=jdatetime.datetime.strptime(issued_at, "%Y/%m/%d")
                    issued_at=issued_at.togregorian()
                except:
                    raise forms.ValidationError(
                        "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            sent_at=row[5]
            if sent_at in ['nan', None, 'None', '']:
                sent_at = None
            else:
                try:
                    sent_at=jdatetime.datetime.strptime(sent_at, "%Y/%m/%d")
                    sent_at=sent_at.togregorian()
                except:
                    raise forms.ValidationError(
                        "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            answered_at=row[6]
            if answered_at in ['nan', None, 'None', '']:
                answered_at = None
            else:
                try:
                    answered_at=jdatetime.datetime.strptime(answered_at, "%Y/%m/%d")
                    answered_at=answered_at.togregorian()
                except:
                    raise forms.ValidationError(
                        "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            verification=row[7]
            if verification in ['nan', None, '']:
                raise forms.ValidationError("ستون نتیجه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            flag=True
            for name, des in VERIFICATION_TYPES:
                if verification == des:
                    verification=name
                    flag=False
            if flag:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون نتیجه در خط " + str(error_line) + " فایل صحیح نیست")

            center=row[8]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            field = row[1]
            doc_type='Order'

            cleaned_data.append((title, doc_type,field, verification, owner, producers_list, issued_at, sent_at, answered_at, center))
        return cleaned_data

    def import_orders(self,excel_data):
        cleaned_data = self.check_orders(excel_data)
        for title, doc_type, field, verification, owner, producers_list, issued_at, sent_at, answered_at, center in cleaned_data:
            order=Order.objects.create(
                title=title,
                field=field,
                verification=verification,
                owner=owner,
                type=doc_type,
                issued_at=issued_at,
                sent_at=sent_at,
                answered_at=answered_at,
                center=center,
            )
            order.judges.set(producers_list)

    def check_seminars(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('S',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            presented_at=row[4]
            if presented_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ ارائه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            assessment_result=row[6]

            participant_number=row[5]
            if participant_number in ['nan', None, 'None', '']:
                participant_number = None
            else:
                try:
                    participant_number = float(participant_number)
                except:
                    raise forms.ValidationError(
                        "فرمت اطلاعات ستون تعداد شرکت کنندگان در خط " + str(error_line) + " فایل صحیح نیست")


            center=row[7]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون ارائه دهندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون ارائه دهندگان در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            field = row[2]
            doc_type='Seminar'

            cleaned_data.append((title,field, organization_code, doc_type,participant_number, producers_list, presented_at, assessment_result, center))
        return cleaned_data

    def import_seminars(self,excel_data):
        cleaned_data = self.check_seminars(excel_data)
        for title, field, organization_code, doc_type,participant_number, producers_list, presented_at, assessment_result, center in cleaned_data:
            seminar=Seminar.objects.create(
                title=title,
                field=field,
                organization_code=organization_code,
                type=doc_type,
                participant_number=participant_number,
                presented_at=presented_at,
                assessment_result=assessment_result,
                center=center,
            )
            seminar.producers.set(producers_list)

    def check_projects(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")

            duration=row[5]
            if duration in ['nan', None, '']:
                raise forms.ValidationError("ستون مدت اجرا در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                duration = float(duration)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون مدت اجرا در خط " + str(error_line) + " فایل صحیح نیست.")

            finished_at=row[4]
            if finished_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تازیخ شروع در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                finished_at=jdatetime.datetime.strptime(finished_at, "%Y/%m/%d")
                finished_at=finished_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            center=row[6]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            manager=row[3]
            if manager in ['nan', None, '']:
                raise forms.ValidationError("ستون مدیر در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                manager_obj, c=Resume.objects.get_or_create(type='Resume', title=manager)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مدیر در خط " + str(error_line) + " فایل صحیح نیست")


            field=row[2]
            doc_type='Project'

            cleaned_data.append((title,organization_code, doc_type, field, manager_obj, finished_at, duration, center))
        return cleaned_data

    def import_projects(self,excel_data):
        cleaned_data = self.check_projects(excel_data)
        for title,organization_code, doc_type, field, manager_obj, finished_at, duration, center in cleaned_data:
            project=Project.objects.create(
                title=title,
                organization_code=organization_code,
                duration=float(duration),
                field=field,
                type=doc_type,
                manager=manager_obj,
                finished_at=finished_at,
                center=center,
            )

    def check_conferences(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            location=row[4]
            if location in ['nan', None, '']:
                raise forms.ValidationError("ستون محل برگزاری در خط " + str(error_line) + " نمی تواند خالی باشد.")

            held_at=row[3]
            if held_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ برگزاری در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                held_at=jdatetime.datetime.strptime(held_at, "%Y/%m/%d")
                held_at=held_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            center=row[5]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            conference_level=row[2]
            if conference_level in ['nan', None, '']:
                raise forms.ValidationError("ستون سطح برگزاری در خط " + str(error_line) + " نمی تواند خالی باشد.")
            flag = True
            for name, des in CONFERENCE_LEVELS:
                if conference_level == des:
                    conference_level=name
                    flag = False
            if flag:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون سطح برگزاری در خط " + str(error_line) + " فایل صحیح نیست")

            field=row[1]
            doc_type='Conference'

            cleaned_data.append((title, location, doc_type, field, held_at, conference_level, center))
        return cleaned_data

    def import_conferences(self,excel_data):
        cleaned_data = self.check_conferences(excel_data)
        for title, location, doc_type, field, held_at, conference_level, center in cleaned_data:
            conference=Conference.objects.create(
                title=title,
                field=field,
                type=doc_type,
                location=location,
                held_at=held_at,
                conference_level=conference_level,
                center=center,
            )

    def check_visits(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            location=row[4]
            if location in ['nan', None, '']:
                raise forms.ValidationError("ستون محل بازدید در خط " + str(error_line) + " نمی تواند خالی باشد.")

            visited_at=row[3]
            if visited_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ بازدید در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                visited_at=jdatetime.datetime.strptime(visited_at, "%Y/%m/%d")
                visited_at=visited_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            center=row[5]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            participant_number=row[2]
            if participant_number in ['nan', None, '']:
                raise forms.ValidationError("ستون تعداد شرکت کنندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                participant_number = float(participant_number)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون تعداد شرکت کنندگان در خط " + str(error_line) + " فایل صحیح نیست")

            field=row[1]
            doc_type='Visit'

            cleaned_data.append((title, location, doc_type, field, visited_at, participant_number, center))
        return cleaned_data

    def import_visits(self,excel_data):
        cleaned_data = self.check_visits(excel_data)
        for title, location, doc_type, field, visited_at, participant_number, center in cleaned_data:
            visit=Visit.objects.create(
                title=title,
                field=field,
                type=doc_type,
                location=location,
                visited_at=visited_at,
                participant_number=participant_number,
                center=center,
            )

    def check_reports(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('R',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            presented_at=row[4]
            if presented_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ ارائه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            related_project=row[5]

            center=row[6]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون تهیه کنندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون تهیه کنندگان در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            field=row[2]
            doc_type='Report'

            cleaned_data.append((title, organization_code,producers_list, doc_type, field, presented_at, related_project, center))
        return cleaned_data

    def import_reports(self,excel_data):
        cleaned_data = self.check_reports(excel_data)
        for title, organization_code,producers_list, doc_type, field, presented_at, related_project, center in cleaned_data:
            report=Report.objects.create(
                title=title,
                organization_code=organization_code,
                field=field,
                type=doc_type,
                presented_at=presented_at,
                related_project=related_project,
                center=center,
            )
            report.producers.set(producers_list)

    def check_resumes(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون نام و نام خانوادگی در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if Resume.objects.filter(title=title).exists():
                raise forms.ValidationError(
                    "ستون نام و نام خانوادگی در خط " + str(error_line) + " نمی تواند تکراری باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '', 'None']:
                raise forms.ValidationError("ستون کد پاسداری در خط " + str(error_line) + " نمی تواند خالی باشد.")

            center=row[5]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            entrance_year=row[2]
            if entrance_year in ['nan', None, '']:
                entrance_year = None
            else:
                try:
                    entrance_year = float(entrance_year)
                except:
                    raise forms.ValidationError(
                        "فرمت اطلاعات ستون سال ورود در خط " + str(error_line) + " فایل صحیح نیست")

            doc_type='Resume'
            measure=row[3]
            degree=row[4]

            cleaned_data.append((title,organization_code, doc_type, entrance_year, measure, degree, center))
        return cleaned_data

    def import_resumes(self,excel_data):
        cleaned_data = self.check_resumes(excel_data)
        for title,organization_code, doc_type, entrance_year, measure, degree, center in cleaned_data:
            resume=Resume.objects.create(
                title=title,
                organization_code=organization_code,
                type=doc_type,
                measure=measure,
                degree=degree,
                entrance_year=entrance_year,
                center=center,
            )

    def check_centers(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                Center.objects.get(title=title)
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند تکراری باشد. مرکزی با این عنوان از قبل وجود دارد.")
            except:
                pass
            
            code=row[1]
            if code in ['nan', None, '']:
                raise forms.ValidationError("ستون کد در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                code=float(code)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون کد در خط " + str(error_line) + " فایل صحیح نیست")

            cleaned_data.append((title, code))
        return cleaned_data

    def import_centers(self,excel_data):
        cleaned_data=self.check_centers(excel_data)
        for title, code in cleaned_data:
            center=Center.objects.create(
                title=title,
                code=code,
            )

    def check_cores(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون نام در خط " + str(error_line) + " نمی تواند خالی باشد.")

            status = row[1]
            if status in ['nan', None, '']:
                raise forms.ValidationError("ستون وضع موجودیت در خط " + str(error_line) + " نمی تواند خالی باشد.")

            manager = row[2]
            if manager in ['nan', None, '']:
                raise forms.ValidationError("ستون مسئول واحد در خط " + str(error_line) + " نمی تواند خالی باشد.")

            contact = row[3]
            if contact in ['nan', None, '']:
                raise forms.ValidationError("ستون شماره تماس در خط " + str(error_line) + " نمی تواند خالی باشد.")

            establish_year = row[4]
            if establish_year in ['nan', None, '']:
                raise forms.ValidationError("ستون سال تاسیس در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                establish_year=float(establish_year)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون سال تاسیس در خط " + str(error_line) + " فایل صحیح نیست")

            activity_field = row[5]
            if activity_field in ['nan', None, '']:
                raise forms.ValidationError("ستون حوزه فعالیت در خط " + str(error_line) + " نمی تواند خالی باشد.")

            professional_field = row[6]
            if professional_field in ['nan', None, '']:
                raise forms.ValidationError("ستون حوزه تخصصی در خط " + str(error_line) + " نمی تواند خالی باشد.")

            number = row[7]
            if number in ['nan', None, '']:
                raise forms.ValidationError("ستون تعداد اعضا در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                number=float(number)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون تعداد اعضا در خط " + str(error_line) + " فایل صحیح نیست")

            doc_type = 'Core'

            cleaned_data.append((title, status, doc_type, number, professional_field, activity_field, establish_year, contact, manager))
        return cleaned_data

    def import_cores(self,excel_data):
        cleaned_data=self.check_cores(excel_data)
        for title, status, doc_type, number, professional_field, activity_field, establish_year, contact, manager in cleaned_data:
            core = Core.objects.create(
                type=doc_type,
                title=title,
                status=status,
                manager=manager,
                contact=contact,
                establish_year=establish_year,
                activity_field=activity_field,
                professional_field=professional_field,
                number=number
                                   )

    def check_techs(self,excel_data):
        error_line=1
        cleaned_data=[]
        for row in excel_data:
            error_line+=1

            title=row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون نام در خط " + str(error_line) + " نمی تواند خالی باشد.")

            status=row[1]
            if status in ['nan', None, '']:
                raise forms.ValidationError("ستون وضع موجودیت در خط " + str(error_line) + " نمی تواند خالی باشد.")

            manager=row[2]
            if manager in ['nan', None, '']:
                raise forms.ValidationError("ستون مسئول واحد در خط " + str(error_line) + " نمی تواند خالی باشد.")

            contact=row[3]
            if contact in ['nan', None, '']:
                raise forms.ValidationError("ستون شماره تماس در خط " + str(error_line) + " نمی تواند خالی باشد.")

            establish_year=row[4]
            if establish_year in ['nan', None, '']:
                raise forms.ValidationError("ستون سال تاسیس در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                establish_year=float(establish_year)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون سال تاسیس در خط " + str(error_line) + " فایل صحیح نیست")

            activity_field=row[5]
            if activity_field in ['nan', None, '']:
                raise forms.ValidationError("ستون حوزه فعالیت در خط " + str(error_line) + " نمی تواند خالی باشد.")

            professional_field=row[6]
            if professional_field in ['nan', None, '']:
                raise forms.ValidationError("ستون حوزه تخصصی در خط " + str(error_line) + " نمی تواند خالی باشد.")

            number=row[7]
            if number in ['nan', None, '']:
                raise forms.ValidationError("ستون تعداد اعضا در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                number=float(number)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون تعداد اعضا در خط " + str(error_line) + " فایل صحیح نیست")

            doc_type='TechUnit'

            cleaned_data.append(
                (title, status, doc_type, number, professional_field, activity_field, establish_year, contact, manager))
        return cleaned_data

    def import_techs(self,excel_data):
        cleaned_data=self.check_techs(excel_data)
        for title, status, doc_type, number, professional_field, activity_field, establish_year, contact, manager in cleaned_data:
            tech=Tech.objects.create(
                type=doc_type,
                title=title,
                status=status,
                manager=manager,
                contact=contact,
                establish_year=establish_year,
                activity_field=activity_field,
                professional_field=professional_field,
                number=number
            )

    def check_companies(self,excel_data):
        error_line=1
        cleaned_data=[]
        for row in excel_data:
            error_line+=1

            title=row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون نام در خط " + str(error_line) + " نمی تواند خالی باشد.")

            status=row[1]
            if status in ['nan', None, '']:
                raise forms.ValidationError("ستون وضع موجودیت در خط " + str(error_line) + " نمی تواند خالی باشد.")

            manager=row[2]
            if manager in ['nan', None, '']:
                raise forms.ValidationError("ستون مسئول واحد در خط " + str(error_line) + " نمی تواند خالی باشد.")

            contact=row[3]
            if contact in ['nan', None, '']:
                raise forms.ValidationError("ستون شماره تماس در خط " + str(error_line) + " نمی تواند خالی باشد.")

            establish_year=row[4]
            if establish_year in ['nan', None, '']:
                raise forms.ValidationError("ستون سال تاسیس در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                establish_year=float(establish_year)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون سال تاسیس در خط " + str(error_line) + " فایل صحیح نیست")

            activity_field=row[5]
            if activity_field in ['nan', None, '']:
                raise forms.ValidationError("ستون حوزه فعالیت در خط " + str(error_line) + " نمی تواند خالی باشد.")

            professional_field=row[6]
            if professional_field in ['nan', None, '']:
                raise forms.ValidationError("ستون حوزه تخصصی در خط " + str(error_line) + " نمی تواند خالی باشد.")

            number=row[7]
            if number in ['nan', None, '']:
                raise forms.ValidationError("ستون تعداد اعضا در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                number=float(number)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون تعداد اعضا در خط " + str(error_line) + " فایل صحیح نیست")

            doc_type='Comapny'

            cleaned_data.append(
                (title, status, doc_type, number, professional_field, activity_field, establish_year, contact, manager))
        return cleaned_data

    def import_companies(self,excel_data):
        cleaned_data=self.check_companies(excel_data)
        for title, status, doc_type, number, professional_field, activity_field, establish_year, contact, manager in cleaned_data:
            company=Company.objects.create(
                type=doc_type,
                title=title,
                status=status,
                manager=manager,
                contact=contact,
                establish_year=establish_year,
                activity_field=activity_field,
                professional_field=professional_field,
                number=number
            )

    def check_futures(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")

            presented_at=row[4]
            if presented_at in ['nan', None, '']:
                presented_at = ''
            else:
                try:
                    presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                    presented_at=presented_at.togregorian()
                except:
                    raise forms.ValidationError(
                        "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            future_type=row[5]
            if future_type in ['nan', None, '']:
                raise forms.ValidationError("ستون نوع آینده پژوهی در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                other_sec = future_type.split('-')
                future_type = other_sec[0]
                other = other_sec[1]
            except:
                future_type = row[5]
                other = None
            flag = True
            for name, des in FUTURE_TYPES:
                if future_type == des:
                    future_type=name
                    flag = False
            if flag:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون نوع آینده پژوهی در خط " + str(error_line) + " فایل صحیح نیست")

            center=row[6]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون ارائه دهندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون ارائه دهندگان در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            field=row[2]
            doc_type='Future'

            cleaned_data.append(
                (title, field, doc_type, producers_list, organization_code, presented_at, future_type, other,center))
        return cleaned_data

    def import_futures(self,excel_data):
        cleaned_data=self.check_futures(excel_data)
        for title, field, doc_type, producers_list, organization_code, presented_at, future_type, other, center in cleaned_data:
            if presented_at:
                future=Future.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    presented_at=presented_at,
                    future_type=future_type,
                    other=other,
                    center=center,
                )
            else:
                future = Future.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    future_type=future_type,
                    other=other,
                    center=center,
                )
            future.producers.set(producers_list)

    def check_journals(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")

            presented_at=row[3]
            if presented_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ چاپ در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            page_number=row[4]
            if page_number in ['nan', None, '']:
                raise forms.ValidationError("ستون تعداد صفحات در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                page_number = float(page_number)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون تعداد صفحات در خط " + str(error_line) + " فایل صحیح نیست")

            field=row[2]
            doc_type='Journal'

            cleaned_data.append(
                (title, field, doc_type, organization_code, presented_at, page_number))
        return cleaned_data

    def import_journals(self,excel_data):
        cleaned_data=self.check_journals(excel_data)
        for title, field, doc_type, organization_code, presented_at, page_number in cleaned_data:
            journal=Journal.objects.create(
                title=title,
                organization_code=organization_code,
                field=field,
                type=doc_type,
                presented_at=presented_at,
                page_number=float(page_number),
            )

    def check_coworks(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            started_at=row[2]
            if started_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ هکاری در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                started_at=jdatetime.datetime.strptime(started_at, "%Y/%m/%d")
                started_at=started_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")


            person_type=row[3]
            if person_type in ['nan', None, '']:
                raise forms.ValidationError("ستون شخض در خط " + str(error_line) + " نمی تواند خالی باشد.")
            flag = True
            for name, des in PERSON_TYPES:
                if person_type == des:
                    person_type=name
                    flag = False
            if flag:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون شخص در خط " + str(error_line) + " فایل صحیح نیست")

            cowork_type=row[4]
            if cowork_type in ['nan', None, 'None', '']:
                cowork_type = None
            else:
                flag = True
                for name, des in COWORK_TYPES:
                    if cowork_type == des:
                        cowork_type=name
                        flag = False
                if flag:
                    raise forms.ValidationError(
                        "فرمت اطلاعات ستون نوع در خط " + str(error_line) + " فایل صحیح نیست")


            center=row[6]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            field=row[1]
            doc_type='Cowork'
            address=row[5]

            cleaned_data.append(
                (title, field, doc_type, cowork_type, person_type, started_at, address, center))
        return cleaned_data

    def import_coworks(self,excel_data):
        cleaned_data=self.check_coworks(excel_data)
        for title, field, doc_type, cowork_type, person_type, started_at, address, center in cleaned_data:
            cowork=CoWork.objects.create(
                title=title,
                person_type=person_type,
                cowork_type=cowork_type,
                field=field,
                started_at=started_at,
                type=doc_type,
                center=center,
                address=address,
            )

    def check_inventions(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code=row[2]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شماره اظهارنامه در خط " + str(error_line) + " نمی تواند خالی باشد.")

            registered_at=row[4]
            if registered_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ ثبت در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                registered_at = jdatetime.datetime.strptime(registered_at, "%Y/%m/%d")
                registered_at = registered_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            project_title=row[1]
            if project_title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان پروژه در خط " + str(error_line) + " نمی تواند خالی باشد.")

            center=row[5]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            if row[3] in ['nan', None, '']:
                raise forms.ValidationError("ستون ارائه دهندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            producers = row[3].split(',')
            producers = producers[:-1]
            if not producers:
                raise forms.ValidationError("فرمت اطلاعات ستون ارائه دهندگان در خط " + str(error_line) + " فایل صحیح نیست")
            producers_list = []
            for producer in producers:
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer.strip())
                producers_list.append(producer_obj)

            doc_type='Invention'

            cleaned_data.append(
                (title, doc_type, organization_code, project_title, registered_at, producers_list, center))
        return cleaned_data

    def import_inventions(self,excel_data):
        cleaned_data=self.check_inventions(excel_data)
        for title, doc_type, organization_code, project_title, registered_at, producers_list, center in cleaned_data:
            invention = Invention.objects.create(
                title=title,
                organization_code=organization_code,
                type=doc_type,
                registered_at=registered_at,
                project_title=project_title,
                center=center,
                                   )
            invention.producers.set(producers_list)

    def check_assessments(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            producer=row[0]
            if producer in ['nan', None, '']:
                raise forms.ValidationError("ستون محقق در خط " + str(error_line) + " نمی تواند خالی باشد.")
            # organization_code=row[1]
            # if organization_code in ['nan', None, '']:
            #     raise forms.ValidationError("ستون کد پاسداری در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون محقق در خط " + str(error_line) + " فایل صحیح نیست")

            # father=row[2]
            # if father in ['nan', None, '']:
            #     raise forms.ValidationError("ستون نام پدر در خط " + str(error_line) + " نمی تواند خالی باشد.")

            scientific_rank=row[1]
            if scientific_rank in ['nan', None, '']:
                raise forms.ValidationError("ستون رتبه علمی در خط " + str(error_line) + " نمی تواند خالی باشد.")

            issue_code=row[2]
            if issue_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شماره داوری در خط " + str(error_line) + " نمی تواند خالی باشد.")

            order_issued_at=row[3]
            if order_issued_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ صدور در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                order_issued_at=jdatetime.datetime.strptime(order_issued_at, "%Y/%m/%d")
                order_issued_at=order_issued_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ صدور در خط " + str(error_line) + " فایل صحیح نیست.")

            elite_received_at=row[4]
            if elite_received_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ دریافت نخبگی در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                elite_received_at=jdatetime.datetime.strptime(elite_received_at, "%Y/%m/%d")
                elite_received_at=elite_received_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ دریافت در خط " + str(error_line) + " فایل صحیح نیست.")

            profile_type=row[5]
            if profile_type in ['nan', None, '']:
                raise forms.ValidationError("ستون نوع پرونده در خط " + str(error_line) + " نمی تواند خالی باشد.")

            center=row[8]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            doc_type='Assessment'
            necessary_condition=row[6]
            sufficient_condition=row[7]

            cleaned_data.append(
                (producer_obj, doc_type, issue_code, scientific_rank, order_issued_at, elite_received_at, profile_type, sufficient_condition, necessary_condition, center))
        return cleaned_data

    def import_assessments(self,excel_data):
        cleaned_data=self.check_assessments(excel_data)
        for producer_obj, doc_type, issue_code, scientific_rank, order_issued_at, elite_received_at, profile_type, sufficient_condition, necessary_condition, center in cleaned_data:
            assessment=Assessment.objects.create(
                type=doc_type,
                producer=producer_obj,
                scientific_rank=scientific_rank,
                issue_code=issue_code,
                profile_type=profile_type,
                necessary_condition=necessary_condition,
                sufficient_condition=sufficient_condition,
                order_issued_at=order_issued_at,
                elite_received_at=elite_received_at,
                center=center,
            )

    def check_workshops(self,excel_data):
        error_line = 1
        cleaned_data = []
        for row in excel_data:
            error_line += 1

            title = row[0]
            if title in ['nan', None, '']:
                raise forms.ValidationError("ستون عنوان در خط " + str(error_line) + " نمی تواند خالی باشد.")

            organization_code = row[1]
            if organization_code in ['nan', None, '']:
                raise forms.ValidationError("ستون شناسه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            if not self.check_organization_code('W',organization_code):
                raise forms.ValidationError("فرمت اطلاعات ستون شناسه در خط " + str(error_line) + " فایل صحیح نیست.")

            workshop_type=row[5]
            if workshop_type in ['nan', None, '']:
                raise forms.ValidationError("ستون نوع کارگاه در خط " + str(error_line) + " نمی تواند خالی باشد.")
            flag = True
            for name, des in WORKSHOP_TYPES:
                if workshop_type == des:
                    workshop_type=name
                    flag = False
            if flag:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون نوع کارگاه در خط " + str(error_line) + " فایل صحیح نیست")


            duration = row[2]
            if duration in ['nan', None, '']:
                raise forms.ValidationError("ستون زمان دوره در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                duration = int(duration)
            except:
                raise forms.ValidationError("فرمت اطلاعات زمان دوره در خط " + str(error_line) + " فایل صحیح نیست.")


            started_at=row[6]
            if started_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ شروع در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                started_at=jdatetime.datetime.strptime(started_at, "%Y/%m/%d")
                started_at=started_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            finished_at=row[7]
            if finished_at in ['nan', None, '']:
                raise forms.ValidationError("ستون تاریخ پایان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                finished_at=jdatetime.datetime.strptime(finished_at, "%Y/%m/%d")
                finished_at=finished_at.togregorian()
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات در ستون تاریخ در خط " + str(error_line) + " فایل صحیح نیست.")

            participant_number=row[8]
            if participant_number in ['nan', None, '']:
                raise forms.ValidationError("ستون تعداد شرکت کنندگان در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                participant_number = float(participant_number)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون تعداد شرکت کنندگان در خط " + str(error_line) + " فایل صحیح نیست")

            location=row[9]
            if location in ['nan', None, '']:
                raise forms.ValidationError("ستون محل برگزاری در خط " + str(error_line) + " نمی تواند خالی باشد.")

            center=row[10]
            if center in ['nan', None, '']:
                raise forms.ValidationError("ستون مرکز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                center = Center.objects.get(title=center)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون مرکز در خط " + str(error_line) + " فایل صحیح نیست")

            producer=row[3]
            if producer in ['nan', None, '']:
                raise forms.ValidationError("ستون ارائه دهنده/کارآموز در خط " + str(error_line) + " نمی تواند خالی باشد.")
            try:
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)
            except:
                raise forms.ValidationError(
                    "فرمت اطلاعات ستون ارائه دهنده/کارآموز در خط " + str(error_line) + " فایل صحیح نیست")

            doc_type='Workshop'

            cleaned_data.append(
                (title, organization_code, doc_type,workshop_type, duration, participant_number, location, started_at, finished_at, producer_obj, center))
        return cleaned_data

    def import_workshops(self,excel_data):
        cleaned_data=self.check_workshops(excel_data)
        for title, organization_code, doc_type,workshop_type, duration, participant_number, location, started_at, finished_at, producer_obj, center in cleaned_data:
            workshop=Workshop.objects.create(
                title=title,
                organization_code=organization_code,
                type=doc_type,
                duration=duration,
                participant_number=participant_number,
                producer=producer_obj,
                started_at=started_at,
                finished_at=finished_at,
                workshop_type=workshop_type,
                location=location,
                center=center,
            )

    def handle_uploaded_file(self, f):
        with open('excel_file.xlsx', 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

    def clean(self):
        cleaned_data = super().clean()
        doc_type = cleaned_data['doc_type']
        try:
            excel_file = cleaned_data['excel_file']
            # self.handle_uploaded_file(excel_file)
        except:
            raise forms.ValidationError("هیچ فایلی انتخاب نشده است.")

        # df = pd.read_csv(excel_file)
        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
        except:
            raise forms.ValidationError("فایل وارد شده فرمت اکسل نیست.")
        # wb = openpyxl.load_workbook(excel_file)
        # worksheet = wb["Sheet1"]

        excel_data = list()
        for row in df.iloc:
            row_data = list()
            for cell in row:
                row_data.append(str(cell))
            excel_data.append(row_data)

        try:
            if doc_type == 'Article':
                self.import_articles(excel_data)
            elif doc_type == 'Book':
                self.import_books(excel_data)
            elif doc_type == 'Experience':
                self.import_experiences(excel_data)
            elif doc_type == 'Idea':
                self.import_ideas(excel_data)
            elif doc_type == 'Thesis':
                self.import_theses(excel_data)
            elif doc_type == 'Manual':
                self.import_manuals(excel_data)
            elif doc_type == 'Order':
                self.import_orders(excel_data)
            elif doc_type == 'Seminar':
                self.import_seminars(excel_data)
            elif doc_type == 'Project':
                self.import_projects(excel_data)
            elif doc_type == 'Conference':
                self.import_conferences(excel_data)
            elif doc_type == 'Visit':
                self.import_visits(excel_data)
            elif doc_type == 'Report':
                self.import_reports(excel_data)
            elif doc_type == 'Resume':
                self.import_resumes(excel_data)
            elif doc_type == 'Center':
                self.import_centers(excel_data)
            elif doc_type == 'Core':
                self.import_cores(excel_data)
            elif doc_type == 'Tech':
                self.import_techs(excel_data)
            elif doc_type == 'Company':
                self.import_companies(excel_data)
            elif doc_type == 'Future':
                self.import_futures(excel_data)
            elif doc_type == 'Journal':
                self.import_journals(excel_data)
            elif doc_type == 'Cowork':
                self.import_coworks(excel_data)
            elif doc_type == 'Invention':
                self.import_inventions(excel_data)
            elif doc_type == 'Assessment':
                self.import_assessments(excel_data)
            elif doc_type == 'Workshop':
                self.import_workshops(excel_data)
        except Exception as e:
            raise forms.ValidationError(e)

        return cleaned_data
