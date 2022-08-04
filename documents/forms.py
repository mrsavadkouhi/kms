import openpyxl
from django import forms
from .models import *
from bootstrap_modal_forms.forms import BSModalModelForm


class DocumentAttachmentForm(BSModalModelForm):
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
        document = Document.objects.get(id=self.cleaned_data['document_id'])
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
            manager_name = row[2]
            manager_name = manager_name.split(' ')
            manger_first_name = manager_name[0]
            if len(manager_name) == 2:
                manger_last_name = manager_name[1]
            else:
                manger_last_name = row[2][len(manager_name)+3:]

            center_name = row[3]

            started_at = row[4]
            if started_at == 'None':
                started_at = ''
            else:
                started_at = datetime.strptime(started_at, "%Y-%m-%d %H:%M:%S")

            to_be_finished = row[5]
            if to_be_finished == 'None':
                to_be_finished = ''
            else:
                to_be_finished = datetime.strptime(to_be_finished, "%Y-%m-%d %H:%M:%S")

            finished_at = row[8]
            if finished_at == 'None':
                finished_at = ''
            else:
                finished_at = datetime.strptime(finished_at, "%Y-%m-%d %H:%M:%S")

            payment = row[6]
            if payment:
                payment = int(payment)
            else:
                payment = 0

            paid = row[7]
            if paid:
                paid = int(paid)
            else:
                paid = 0

            status = row[9]

            try:
                center = Center.objects.get(name=center_name)
                manager = Profile.objects.get(user__first_name=manger_first_name,user__last_name=manger_last_name)
                Project.objects.create(name=row[0], description=row[1], manager=manager, center=center, started_at=started_at, finished_at=finished_at, to_be_finished=to_be_finished, payment=payment, paid=paid, status=status)
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
            pass
        elif doc_type == 'Experience':
            pass
        elif doc_type == 'Idea':
            pass
        elif doc_type == 'Thesis':
            pass
        elif doc_type == 'Manual':
            pass
        elif doc_type == 'Order':
            pass
        elif doc_type == 'Seminar':
            pass
        elif doc_type == 'Project':
            pass
        elif doc_type == 'Conference':
            pass
        elif doc_type == 'Visit':
            pass
        elif doc_type == 'Report':
            pass
        elif doc_type == 'Resume':
            pass
        elif doc_type == 'Center':
            pass
        elif doc_type == 'Core':
            pass
        elif doc_type == 'Tech':
            pass
        elif doc_type == 'Company':
            pass
        elif doc_type == 'Future':
            pass
        elif doc_type == 'Journal':
            pass
        elif doc_type == 'Cowork':
            pass
        elif doc_type == 'Invention':
            pass
        elif doc_type == 'Assessment':
            pass
        elif doc_type == 'Workshop':
            pass

        return cleaned_data
