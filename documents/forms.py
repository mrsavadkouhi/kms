import jdatetime
import openpyxl
from django import forms
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

    def import_articles(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_books(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_experiences(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_ideas(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_theses(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_manuals(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_orders(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_seminars(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_projects(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_conferences(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_visits(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_reports(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_resumes(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_centers(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_cores(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_techs(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_companies(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_futures(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_journals(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_coworks(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_inventions(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_assessments(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def import_workshops(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code = row[1]
            field = row[2]
            doc_type = 'Article'
            key_words = row[3]
            published_at=row[6]
            publish_title=row[9]
            center=row[10]

            producers_raw = row[4].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            judges_raw = row[5].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            publish_type = row[7]
            for name, des in ARTICLE_PUBLISH_TYPES:
                if publish_type == des:
                    publish_type = name

            publish_level = row[8]
            for name, des in ARTICLE_PUBLISH_LEVELS:
                if publish_level == des:
                    publish_level = name

            try:
                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)
                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

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
                article.judges.set(judges_list)
            except:
                pass

    def clean(self):
        cleaned_data = super().clean()
        doc_type = cleaned_data['doc_type']

        excel_file = cleaned_data['excel_file']

        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]

        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        if doc_type == 'Article':
            self.import_articles(excel_data[1:])
        elif doc_type == 'Book':
            self.import_books(excel_data[1:])
        elif doc_type == 'Experience':
            self.import_experiences(excel_data[1:])
        elif doc_type == 'Idea':
            self.import_ideas(excel_data[1:])
        elif doc_type == 'Thesis':
            self.import_theses(excel_data[1:])
        elif doc_type == 'Manual':
            self.import_manuals(excel_data[1:])
        elif doc_type == 'Order':
            self.import_orders(excel_data[1:])
        elif doc_type == 'Seminar':
            self.import_seminars(excel_data[1:])
        elif doc_type == 'Project':
            self.import_projects(excel_data[1:])
        elif doc_type == 'Conference':
            self.import_conferences(excel_data[1:])
        elif doc_type == 'Visit':
            self.import_visits(excel_data[1:])
        elif doc_type == 'Report':
            self.import_reports(excel_data[1:])
        elif doc_type == 'Resume':
            self.import_resumes(excel_data[1:])
        elif doc_type == 'Center':
            self.import_centers(excel_data[1:])
        elif doc_type == 'Core':
            self.import_cores(excel_data[1:])
        elif doc_type == 'Tech':
            self.import_techs(excel_data[1:])
        elif doc_type == 'Company':
            self.import_companies(excel_data[1:])
        elif doc_type == 'Future':
            self.import_futures(excel_data[1:])
        elif doc_type == 'Journal':
            self.import_journals(excel_data[1:])
        elif doc_type == 'Cowork':
            self.import_coworks(excel_data[1:])
        elif doc_type == 'Invention':
            self.import_inventions(excel_data[1:])
        elif doc_type == 'Assessment':
            self.import_assessments(excel_data[1:])
        elif doc_type == 'Workshop':
            self.import_workshops(excel_data[1:])

        return cleaned_data
