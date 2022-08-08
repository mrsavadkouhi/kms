import jdatetime
import openpyxl
import csv
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
            doc_type = 'Book'
            published_at=row[7]
            publisher = row[6]
            assessment_result=row[9]
            fipa=row[5]
            center=row[10]

            producer = row[3]

            judges_raw = row[8].split(',')
            judges_raw = judges_raw[:-1]
            judges = []
            for judge in judges_raw:
                judge = judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)


                center = Center.objects.get(title=center)
                published_at = jdatetime.datetime.strptime(published_at, "%Y/%m/%d")
                published_at = published_at.togregorian()
                producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer)

                judges_list = []
                for judge in judges:
                    judge_obj, c = Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

                book = Book.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    publisher=publisher,
                    fipa=fipa,
                    producer=producer_obj,
                    published_at=published_at,
                    assessment_result=assessment_result,
                    center=center,
                                       )
                book.judges.set(judges_list)

    def import_experiences(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Experience'
            presented_at=row[5]
            assessment_result=row[7]
            center=row[8]

            producer=row[3]

            judges_raw=row[6].split(',')
            judges_raw=judges_raw[:-1]
            judges=[]
            for judge in judges_raw:
                judge=judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            try:
                center=Center.objects.get(title=center)
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                judges_list=[]
                for judge in judges:
                    judge_obj, c=Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

                experience=Experience.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    producer=producer_obj,
                    presented_at=presented_at,
                    assessment_result=assessment_result,
                    center=center,
                )
                experience.judges.set(judges_list)
            except:
                pass

    def import_ideas(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Idea'
            presented_at=row[5]
            assessment_result=row[7]
            center=row[8]

            producer=row[3]

            judges_raw=row[6].split(',')
            judges_raw=judges_raw[:-1]
            judges=[]
            for judge in judges_raw:
                judge=judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            try:
                center=Center.objects.get(title=center)
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                judges_list=[]
                for judge in judges:
                    judge_obj, c=Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

                idea=Idea.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    producer=producer_obj,
                    presented_at=presented_at,
                    assessment_result=assessment_result,
                    center=center,
                )
                idea.judges.set(judges_list)
            except:
                pass

    def import_theses(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Thesis'
            measure=row[4]
            degree=row[5]
            university=row[6]
            presented_at=row[7]
            center=row[8]
            producer=row[3]

            try:
                center=Center.objects.get(title=center)
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                thesis=Thesis.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    producer=producer_obj,
                    presented_at=presented_at,
                    measure=measure,
                    degree=degree,
                    university=university,
                    center=center,
                )
            except:
                pass

    def import_manuals(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Manual'
            declared_at=row[4]
            center=row[5]
            producer=row[3]

            try:
                center=Center.objects.get(title=center)
                declared_at=jdatetime.datetime.strptime(declared_at, "%Y/%m/%d")
                declared_at=declared_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                manual=Manual.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    producer=producer_obj,
                    declared_at=declared_at,
                    center=center,
                )
            except:
                pass

    def import_orders(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Order'
            issued_at=row[4]
            center=row[5]
            receiver=row[3]

            try:
                center=Center.objects.get(title=center)
                issued_at=jdatetime.datetime.strptime(issued_at, "%Y/%m/%d")
                issued_at=issued_at.togregorian()
                receiver_obj, c=Resume.objects.get_or_create(type='Resume', title=receiver)

                order=Order.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    receiver=receiver_obj,
                    issued_at=issued_at,
                    center=center,
                )
            except:
                pass

    def import_seminars(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Seminar'
            presented_at=row[5]
            participant_number=row[6]
            assessment_result=row[8]
            center=row[9]
            producer=row[3]

            judges_raw=row[7].split(',')
            judges_raw=judges_raw[:-1]
            judges=[]
            for judge in judges_raw:
                judge=judge.strip()
                detail=judge.split('-')
                judge=(detail[1], detail[0])
                judges.append(judge)

            try:
                center=Center.objects.get(title=center)
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                judges_list=[]
                for judge in judges:
                    judge_obj, c=Resume.objects.get_or_create(type='Resume', title=judge[1], organization_code=judge[0])
                    judges_list.append(judge_obj)

                seminar=Seminar.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    producer=producer_obj,
                    participant_number=int(participant_number),
                    presented_at=presented_at,
                    assessment_result=assessment_result,
                    center=center,
                )
                seminar.judges.set(judges_list)
            except:
                pass

    def import_projects(self, excel_data):
        for row in excel_data:
            title=row[0]
            field=row[1]
            doc_type='Project'
            duration=row[4]
            finished_at=row[3]
            center=row[5]
            manager=row[2]

            try:
                center=Center.objects.get(title=center)
                finished_at=jdatetime.datetime.strptime(finished_at, "%Y/%m/%d")
                finished_at=finished_at.togregorian()
                manager_obj, c=Resume.objects.get_or_create(type='Resume', title=manager)

                project=Project.objects.create(
                    title=title,
                    duration=int(duration),
                    field=field,
                    type=doc_type,
                    manager=manager_obj,
                    finished_at=finished_at,
                    center=center,
                )
            except:
                pass

    def import_conferences(self, excel_data):
        for row in excel_data:
            title=row[0]
            field=row[1]
            doc_type='Conference'
            location=row[4]
            held_at=row[3]
            center=row[5]

            conference_level=row[2]
            for name, des in CONFERENCE_LEVELS:
                if conference_level == des:
                    conference_level=name

            try:
                center=Center.objects.get(title=center)
                held_at=jdatetime.datetime.strptime(held_at, "%Y/%m/%d")
                held_at=held_at.togregorian()

                conference=Conference.objects.create(
                    title=title,
                    field=field,
                    type=doc_type,
                    location=location,
                    held_at=held_at,
                    conference_level=conference_level,
                    center=center,
                )
            except:
                pass

    def import_visits(self, excel_data):
        for row in excel_data:
            title=row[0]
            field=row[1]
            doc_type='Visit'
            location=row[4]
            visited_at=row[3]
            center=row[5]
            participant_number=row[2]

            try:
                center=Center.objects.get(title=center)
                visited_at=jdatetime.datetime.strptime(visited_at, "%Y/%m/%d")
                visited_at=visited_at.togregorian()

                visit=Visit.objects.create(
                    title=title,
                    field=field,
                    type=doc_type,
                    location=location,
                    visited_at=visited_at,
                    participant_number=int(participant_number),
                    center=center,
                )
            except:
                pass

    def import_reports(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Report'
            presented_at=row[4]
            related_project=row[5]
            center=row[6]
            producer=row[3]

            try:
                center=Center.objects.get(title=center)
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                report=Report.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    producer=producer_obj,
                    presented_at=presented_at,
                    related_project=related_project,
                    center=center,
                )
            except:
                pass

    def import_resumes(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            doc_type='Resume'
            entrance_year=row[2]
            measure=row[3]
            degree=row[4]
            center=row[5]

            try:
                center=Center.objects.get(title=center)

                resume=Resume.objects.create(
                    title=title,
                    organization_code=organization_code,
                    type=doc_type,
                    measure=measure,
                    degree=degree,
                    entrance_year=int(entrance_year),
                    center=center,
                )
            except:
                pass

    def import_centers(self, excel_data):
        for row in excel_data:
            title=row[0]
            code=row[1]

            try:
                center=Center.objects.create(
                    title=title,
                    code=code,
                )
            except:
                pass

    def import_cores(self, excel_data):
        for row in excel_data:
            title = row[0]
            status = row[1]
            manager = row[2]
            contact = row[3]
            establish_year = row[4]
            activity_field = row[5]
            professional_field = row[6]
            number = row[7]
            doc_type = 'Core'

            try:
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
            except:
                pass

    def import_techs(self, excel_data):
        for row in excel_data:
            title=row[0]
            status=row[1]
            manager=row[2]
            contact=row[3]
            establish_year=row[4]
            activity_field=row[5]
            professional_field=row[6]
            number=row[7]
            doc_type='TechUnit'

            try:
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
            except:
                pass

    def import_companies(self, excel_data):
        for row in excel_data:
            title=row[0]
            status=row[1]
            manager=row[2]
            contact=row[3]
            establish_year=row[4]
            activity_field=row[5]
            professional_field=row[6]
            number=row[7]
            doc_type='Comapny'

            try:
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
            except:
                pass

    def import_futures(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Future'
            presented_at=row[4]
            future_type=row[5]
            for name, des in FUTURE_TYPES:
                if future_type == des:
                    future_type=name
            center=row[6]
            producer=row[3]

            try:
                center=Center.objects.get(title=center)
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                future=Future.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    producer=producer_obj,
                    presented_at=presented_at,
                    future_type=future_type,
                    center=center,
                )
            except:
                pass

    def import_journals(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Journal'
            presented_at=row[3]
            page_number=row[4]

            try:
                presented_at=jdatetime.datetime.strptime(presented_at, "%Y/%m/%d")
                presented_at=presented_at.togregorian()

                journal=Journal.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    presented_at=presented_at,
                    page_number=int(page_number),
                )
            except:
                pass

    def import_coworks(self, excel_data):
        for row in excel_data:
            title=row[0]
            field=row[1]
            doc_type='Cowork'
            person_type=row[2]
            for name, des in PERSON_TYPES:
                if person_type == des:
                    person_type=name
            cowork_type=row[3]
            for name, des in COWORK_TYPES:
                if cowork_type == des:
                    cowork_type=name
            address=row[4]
            center=row[5]

            try:
                center=Center.objects.get(title=center)

                cowork=CoWork.objects.create(
                    title=title,
                    person_type=person_type,
                    cowork_type=cowork_type,
                    field=field,
                    type=doc_type,
                    center=center,
                    address=address,
                )
            except:
                pass

    def import_inventions(self, excel_data):
        for row in excel_data:
            title = row[0]
            organization_code=row[2]
            doc_type = 'Invention'
            registered_at=row[4]
            project_title=row[1]
            center=row[5]

            producers_raw = row[3].split(',')
            producers_raw = producers_raw[:-1]
            producers = []
            for producer in producers_raw:
                producer = producer.strip()
                detail = producer.split('-')
                producer = (detail[1], detail[0])
                producers.append(producer)

            try:
                center = Center.objects.get(title=center)
                registered_at = jdatetime.datetime.strptime(registered_at, "%Y/%m/%d")
                registered_at = registered_at.togregorian()

                producers_list = []
                for producer in producers:
                    producer_obj, c = Resume.objects.get_or_create(type='Resume', title=producer[1], organization_code=producer[0])
                    producers_list.append(producer_obj)

                invention = Invention.objects.create(
                    title=title,
                    organization_code=organization_code,
                    type=doc_type,
                    registered_at=registered_at,
                    project_title=project_title,
                    center=center,
                                       )
                invention.producers.set(producers_list)
            except:
                pass

    def import_assessments(self, excel_data):
        for row in excel_data:
            producer=row[0]
            father=row[2]
            scientific_rank=row[3]
            doc_type='Assessment'
            issue_code=row[4]
            order_issued_at=row[5]
            elite_received_at=row[6]
            profile_type=row[7]
            necessary_condition=row[8]
            sufficient_condition=row[9]
            center=row[10]

            try:
                center=Center.objects.get(title=center)
                order_issued_at=jdatetime.datetime.strptime(order_issued_at, "%Y/%m/%d")
                order_issued_at=order_issued_at.togregorian()
                elite_received_at=jdatetime.datetime.strptime(elite_received_at, "%Y/%m/%d")
                elite_received_at=elite_received_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                assessment=Assessment.objects.create(
                    type=doc_type,
                    father=father,
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
            except:
                pass

    def import_workshops(self, excel_data):
        for row in excel_data:
            title=row[0]
            organization_code=row[1]
            field=row[2]
            doc_type='Workshop'
            workshop_type=row[5]
            for name, des in WORKSHOP_TYPES:
                if workshop_type == des:
                    workshop_type = name
            started_at=row[6]
            meeting_number=row[7]
            participant_number=row[8]
            location=row[9]
            center=row[10]
            producer=row[3]

            try:
                center=Center.objects.get(title=center)
                started_at=jdatetime.datetime.strptime(started_at, "%Y/%m/%d")
                started_at=started_at.togregorian()
                producer_obj, c=Resume.objects.get_or_create(type='Resume', title=producer)

                workshop=Workshop.objects.create(
                    title=title,
                    organization_code=organization_code,
                    field=field,
                    type=doc_type,
                    producer=producer_obj,
                    started_at=started_at,
                    workshop_type=workshop_type,
                    location=location,
                    meeting_number=int(meeting_number),
                    participant_number=int(participant_number),
                    center=center,
                )
            except:
                pass

    def clean(self):
        cleaned_data = super().clean()
        doc_type = cleaned_data['doc_type']
        try:
            excel_file = cleaned_data['excel_file']
        except:
            raise forms.ValidationError("هیچ فایلی انتخاب نشده است.")

        wb = openpyxl.load_workbook(excel_file)
        worksheet = wb["Sheet1"]

        excel_data = list()
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)

        try:
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
        except:
            raise forms.ValidationError("فرمت اطلاعات فایل وارد شده صحیح نیست. مجددا بررسی نمایید.")

        return cleaned_data
