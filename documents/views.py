
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, TemplateView, FormView, ListView
from .json_mixin import *

from .models import *
from .forms import *
from bootstrap_modal_forms.generic import BSModalCreateView


class DocumentAttachmentCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'attach_form.html'
    model = DocumentAttachment
    form_class = DocumentAttachmentForm

    def get_success_url(self):
        doc = Document.objects.get(id=self.kwargs['pk'])
        if doc.type == 'Article':
            return reverse_lazy('documents:article_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Book':
            return reverse_lazy('documents:book_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Resume':
            return reverse_lazy('documents:resume_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Experience':
            return reverse_lazy('documents:experience_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Thesis':
            return reverse_lazy('documents:thesis_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Idea':
            return reverse_lazy('documents:idea_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Seminar':
            return reverse_lazy('documents:seminar_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Workshop':
            return reverse_lazy('documents:workshop_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Conference':
            return reverse_lazy('documents:conference_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Visit':
            return reverse_lazy('documents:visit_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Project':
            return reverse_lazy('documents:project_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Manual':
            return reverse_lazy('documents:manual_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Report':
            return reverse_lazy('documents:report_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Journal':
            return reverse_lazy('documents:journal_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Future':
            return reverse_lazy('documents:future_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'CoWork':
            return reverse_lazy('documents:cowork_details', kwargs={'pk': self.kwargs['pk']})


class CoreAttachmentCreateView(LoginRequiredMixin, BSModalCreateView):
    template_name = 'core_attach_form.html'
    model = DocumentAttachment
    form_class = CenterAttachmentForm

    def get_success_url(self):
        doc = CenterData.objects.get(id=self.kwargs['pk'])
        if doc.type == 'Core':
            return reverse_lazy('documents:core_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'TechUnit':
            return reverse_lazy('documents:tech_details', kwargs={'pk': self.kwargs['pk']})
        elif doc.type == 'Company':
            return reverse_lazy('documents:company_details', kwargs={'pk': self.kwargs['pk']})


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


class CenterListView(LoginRequiredMixin, ListView):
    model=Center
    template_name='center/center_list.html'


class CenterCreateView(LoginRequiredMixin, CreateView):
    model=Center
    template_name='center/center_form.html'
    form_class=CenterForm
    success_url=reverse_lazy('documents:center_list')
    extra_context={
        'title': 'create',
    }


class CenterDetailsView(LoginRequiredMixin, DetailView):
    model=Center
    template_name='center/center_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['object_list']= []
        context['article_num']= 0
        context['book_num']= 0
        context['idea_num']= 0
        context['exp_num']= 0
        context['manual_num']= 0
        context['seminar_num']= 0
        context['conf_num']= 0
        context['project_num']= 0
        context['visit_num']= 0
        context['report_num']= 0
        context['order_num']= 0
        context['thesis_num']= 0
        context['resume_num']= 0

        for item in self.object.center.all():
            if item.type == 'Resume':
                context['resume_num']+=1
                context['object_list'].append(item)
            if item.type == 'Article':
                context['article_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Book':
                context['book_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Idea':
                context['idea_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Experience':
                context['exp_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Manual':
                context['manual_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Seminar':
                context['seminar_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Thesis':
                context['thesis_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Conference':
                context['conf_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Visit':
                context['visit_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Project':
                context['project_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Order':
                context['order_num']+=1
                context['object_list'].append(item)
            elif item.type == 'Report':
                context['report_num']+=1
                context['object_list'].append(item)

        return context


class CenterUpdateForm(LoginRequiredMixin, UpdateView):
    model=Center
    template_name='center/center_form.html'
    form_class=CenterForm
    success_url=reverse_lazy('documents:center_list')
    extra_context={
        'title': 'update',
    }


class CenterDeleteView(LoginRequiredMixin, JSONDeleteView):
    model=Center


class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = 'article/article_list.html'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article/article_form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('documents:article_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        context['types'] = ARTICLE_PUBLISH_TYPES
        context['mag_levels']=ARTICLE_MAGANIZE_PUBLISH_LEVELS
        context['con_levels']=ARTICLE_CONFERENCE_PUBLISH_LEVELS
        # context['fields'] = DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class ArticleDetailsView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article/article_detail.html'


class ArticleUpdateForm(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'article/article_form.html'
    form_class = ArticleForm
    success_url = reverse_lazy('documents:article_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        context['types']=ARTICLE_PUBLISH_TYPES
        context['mag_levels']=ARTICLE_MAGANIZE_PUBLISH_LEVELS
        context['con_levels']=ARTICLE_CONFERENCE_PUBLISH_LEVELS
        # context['fields']=DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class ArticleDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Article


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book/book_list.html'


class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'book/book_form.html'
    form_class = BookForm
    success_url = reverse_lazy('documents:book_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class BookDetailsView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'book/book_detail.html'


class BookUpdateForm(LoginRequiredMixin, UpdateView):
    model = Book
    template_name = 'book/book_form.html'
    form_class = BookForm
    success_url = reverse_lazy('documents:book_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class BookDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Book


class ExperienceListView(LoginRequiredMixin, ListView):
    model = Experience
    template_name = 'experience/experience_list.html'


class ExperienceCreateView(LoginRequiredMixin, CreateView):
    model = Experience
    template_name = 'experience/experience_form.html'
    form_class = ExperienceForm
    success_url = reverse_lazy('documents:experience_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class ExperienceDetailsView(LoginRequiredMixin, DetailView):
    model = Experience
    template_name = 'experience/experience_detail.html'


class ExperienceUpdateForm(LoginRequiredMixin, UpdateView):
    model = Experience
    template_name = 'experience/experience_form.html'
    form_class = ExperienceForm
    success_url = reverse_lazy('documents:experience_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class ExperienceDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Experience


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    template_name = 'order/order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('documents:order_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        return context


class OrderDetailsView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'


class OrderUpdateForm(LoginRequiredMixin, UpdateView):
    model = Order
    template_name = 'order/order_form.html'
    form_class = OrderForm
    success_url = reverse_lazy('documents:order_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        return context


class OrderDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Order


class InventionListView(LoginRequiredMixin, ListView):
    model = Invention
    template_name = 'invention/invention_list.html'


class InventionCreateView(LoginRequiredMixin, CreateView):
    model = Invention
    template_name = 'invention/invention_form.html'
    form_class = InventionForm
    success_url = reverse_lazy('documents:invention_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        return context


class InventionDetailsView(LoginRequiredMixin, DetailView):
    model = Invention
    template_name = 'invention/invention_detail.html'


class InventionUpdateForm(LoginRequiredMixin, UpdateView):
    model = Invention
    template_name = 'invention/invention_form.html'
    form_class = InventionForm
    success_url = reverse_lazy('documents:invention_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        return context


class InventionDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Invention


class AssessmentListView(LoginRequiredMixin, ListView):
    model = Assessment
    template_name = 'assessment/assessment_list.html'


class AssessmentCreateView(LoginRequiredMixin, CreateView):
    model = Assessment
    template_name = 'assessment/assessment_form.html'
    form_class = AssessmentForm
    success_url = reverse_lazy('documents:assessment_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        return context


class AssessmentDetailsView(LoginRequiredMixin, DetailView):
    model = Assessment
    template_name = 'assessment/assessment_detail.html'


class AssessmentUpdateForm(LoginRequiredMixin, UpdateView):
    model = Assessment
    template_name = 'assessment/assessment_form.html'
    form_class = AssessmentForm
    success_url = reverse_lazy('documents:assessment_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        return context


class AssessmentDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Assessment


class IdeaListView(LoginRequiredMixin, ListView):
    model = Idea
    template_name = 'idea/idea_list.html'


class IdeaCreateView(LoginRequiredMixin, CreateView):
    model = Idea
    template_name = 'idea/idea_form.html'
    form_class = IdeaForm
    success_url = reverse_lazy('documents:idea_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class IdeaDetailsView(LoginRequiredMixin, DetailView):
    model = Idea
    template_name = 'idea/idea_detail.html'


class IdeaUpdateForm(LoginRequiredMixin, UpdateView):
    model = Idea
    template_name = 'idea/idea_form.html'
    form_class = IdeaForm
    success_url = reverse_lazy('documents:idea_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class IdeaDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Idea


class SeminarListView(LoginRequiredMixin, ListView):
    model = Seminar
    template_name = 'seminar/seminar_list.html'


class SeminarCreateView(LoginRequiredMixin, CreateView):
    model = Seminar
    template_name = 'seminar/seminar_form.html'
    form_class = SeminarForm
    success_url = reverse_lazy('documents:seminar_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class SeminarDetailsView(LoginRequiredMixin, DetailView):
    model = Seminar
    template_name = 'seminar/seminar_detail.html'


class SeminarUpdateForm(LoginRequiredMixin, UpdateView):
    model = Seminar
    template_name = 'seminar/seminar_form.html'
    form_class = SeminarForm
    success_url = reverse_lazy('documents:seminar_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class SeminarDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Seminar


class WorkshopListView(LoginRequiredMixin, ListView):
    model = Workshop
    template_name = 'workshop/workshop_list.html'


class WorkshopCreateView(LoginRequiredMixin, CreateView):
    model = Workshop
    template_name = 'workshop/workshop_form.html'
    form_class = WorkshopForm
    success_url = reverse_lazy('documents:workshop_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['workshop_types']=WORKSHOP_TYPES
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class WorkshopDetailsView(LoginRequiredMixin, DetailView):
    model = Workshop
    template_name = 'workshop/workshop_detail.html'


class WorkshopUpdateForm(LoginRequiredMixin, UpdateView):
    model = Workshop
    template_name = 'workshop/workshop_form.html'
    form_class = WorkshopForm
    success_url = reverse_lazy('documents:workshop_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['workshop_types']=WORKSHOP_TYPES
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class WorkshopDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Workshop


class ConferenceListView(LoginRequiredMixin, ListView):
    model = Conference
    template_name = 'conference/conference_list.html'


class ConferenceCreateView(LoginRequiredMixin, CreateView):
    model = Conference
    template_name = 'conference/conference_form.html'
    form_class = ConferenceForm
    success_url = reverse_lazy('documents:conference_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['conference_levels']=CONFERENCE_LEVELS
        return context


class ConferenceDetailsView(LoginRequiredMixin, DetailView):
    model = Conference
    template_name = 'conference/conference_detail.html'


class ConferenceUpdateForm(LoginRequiredMixin, UpdateView):
    model = Conference
    template_name = 'conference/conference_form.html'
    form_class = ConferenceForm
    success_url = reverse_lazy('documents:conference_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['conference_levels']=CONFERENCE_LEVELS
        return context


class ConferenceDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Conference


class VisitListView(LoginRequiredMixin, ListView):
    model = Visit
    template_name = 'visit/visit_list.html'


class VisitCreateView(LoginRequiredMixin, CreateView):
    model = Visit
    template_name = 'visit/visit_form.html'
    form_class = VisitForm
    success_url = reverse_lazy('documents:visit_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        return context


class VisitDetailsView(LoginRequiredMixin, DetailView):
    model = Visit
    template_name = 'visit/visit_detail.html'


class VisitUpdateForm(LoginRequiredMixin, UpdateView):
    model = Visit
    template_name = 'visit/visit_form.html'
    form_class = VisitForm
    success_url = reverse_lazy('documents:visit_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        return context


class VisitDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Visit


class ThesisListView(LoginRequiredMixin, ListView):
    model = Thesis
    template_name = 'thesis/thesis_list.html'


class ThesisCreateView(LoginRequiredMixin, CreateView):
    model = Thesis
    template_name = 'thesis/thesis_form.html'
    form_class = ThesisForm
    success_url = reverse_lazy('documents:thesis_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes'] = Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        return context


class ThesisDetailsView(LoginRequiredMixin, DetailView):
    model = Thesis
    template_name = 'thesis/thesis_detail.html'


class ThesisUpdateForm(LoginRequiredMixin, UpdateView):
    model = Thesis
    template_name = 'thesis/thesis_form.html'
    form_class = ThesisForm
    success_url = reverse_lazy('documents:thesis_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        return context


class ThesisDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Thesis


class ResumeListView(LoginRequiredMixin, ListView):
    model = Resume
    template_name = 'resume/resume_list.html'


class ResumeCreateView(LoginRequiredMixin, CreateView):
    model = Resume
    template_name = 'resume/resume_form.html'
    form_class = ResumeForm
    success_url = reverse_lazy('documents:resume_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        context['profiles']=Profile.objects.all()
        return context


class ResumeDetailsView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'resume/resume_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['object_list']= []
        context['article_num']= 0
        context['book_num']= 0
        context['idea_num']= 0
        context['judge_num']= 0
        context['exp_num']= 0
        context['manual_num']= 0
        context['order_num']= 0
        context['project_num']= 0
        context['report_num']= 0
        context['seminar_num']= 0
        context['thesis_num']= 0

        for item in self.object.idea_producer.all():
            context['object_list'].append((item, '????????', item.presented_at))
            context['idea_num']+=1
        for item in self.object.book_producer.all():
            context['object_list'].append((item, '????????', item.published_at))
            context['book_num']+=1
        for item in self.object.experience_producer.all():
            context['object_list'].append((item, '??????????', item.presented_at))
            context['exp_num']+=1
        for item in self.object.thesis_producer.all():
            context['object_list'].append((item, '?????????? ????????', item.presented_at))
            context['thesis_num']+=1
        for item in self.object.manual_producer.all():
            context['object_list'].append((item, '????????????????????', item.declared_at))
            context['manual_num']+=1
        for item in self.object.order_receiver.all():
            context['object_list'].append((item, '??????????', item.issued_at))
            context['order_num']+=1
        for item in self.object.seminar_producer.all():
            context['object_list'].append((item, '????????????', item.presented_at))
            context['seminar_num']+=1
        for item in self.object.report_producer.all():
            context['object_list'].append((item, '??????????', item.presented_at))
            context['report_num']+=1
        for item in self.object.project_manager.all():
            context['object_list'].append((item, '??????????', item.finished_at))
            context['project_num']+=1
        for item in self.object.article_producers.all():
            context['object_list'].append((item, '??????????', item.published_at))
            context['article_num']+=1

        for item in self.object.idea_judges.all():
            context['object_list'].append((item, '??????????', item.presented_at))
            context['judge_num']+=1
        for item in self.object.book_judges.all():
            context['object_list'].append((item, '??????????', item.published_at))
            context['judge_num']+=1
        for item in self.object.experience_judges.all():
            context['object_list'].append((item, '??????????', item.presented_at))
            context['judge_num']+=1
        for item in self.object.seminar_judges.all():
            context['object_list'].append((item, '??????????', item.presented_at))
            context['judge_num']+=1
        for item in self.object.article_judges.all():
            context['object_list'].append((item, '??????????', item.published_at))
            context['judge_num']+=1

        return context


class ResumeUpdateForm(LoginRequiredMixin, UpdateView):
    model = Resume
    template_name = 'resume/resume_form.html'
    form_class = ResumeForm
    success_url = reverse_lazy('documents:resume_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        context['profiles']=Profile.objects.all()
        return context


class ResumeDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Resume


class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'project/project_list.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    template_name = 'project/project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('documents:project_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        return context


class ProjectDetailsView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project/project_detail.html'


class ProjectUpdateForm(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'project/project_form.html'
    form_class = ProjectForm
    success_url = reverse_lazy('documents:project_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        return context


class ProjectDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Project


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'report/report_list.html'


class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    template_name = 'report/report_form.html'
    form_class = ReportForm
    success_url = reverse_lazy('documents:report_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        # context['projects']=Document.objects.filter(type="Project")
        context['centers']= Center.objects.all()
        # # context['fields'] = DOCUMENT_FIELDS
        context['years']=['pre98', '98', '99']
        for i in range(400, 430):
            context['years'].append(str(i))
        return context


class ReportDetailsView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'report/report_detail.html'


class ReportUpdateForm(LoginRequiredMixin, UpdateView):
    model = Report
    template_name = 'report/report_form.html'
    form_class = ReportForm
    success_url = reverse_lazy('documents:report_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        # context['projects']=Document.objects.filter(type="Project")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['years']=['pre98', '98', '99']
        for i in range(400, 430):
            context['years'].append(str(i))
        return context


class ReportDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Report


class ManualListView(LoginRequiredMixin, ListView):
    model = Manual
    template_name = 'manual/manual_list.html'


class ManualCreateView(LoginRequiredMixin, CreateView):
    model = Manual
    template_name = 'manual/manual_form.html'
    form_class = ManualForm
    success_url = reverse_lazy('documents:manual_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class ManualDetailsView(LoginRequiredMixin, DetailView):
    model = Manual
    template_name = 'manual/manual_detail.html'


class ManualUpdateForm(LoginRequiredMixin, UpdateView):
    model = Manual
    template_name = 'manual/manual_form.html'
    form_class = ManualForm
    success_url = reverse_lazy('documents:manual_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['years'] = ['pre98','98','99']
        for i in range(400,430):
            context['years'].append(str(i))
        return context


class ManualDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Manual


class JournalListView(LoginRequiredMixin, ListView):
    model = Journal
    template_name = 'journal/journal_list.html'


class JournalCreateView(LoginRequiredMixin, CreateView):
    model = Journal
    template_name = 'journal/journal_form.html'
    form_class = JournalForm
    success_url = reverse_lazy('documents:journal_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        return context


class JournalDetailsView(LoginRequiredMixin, DetailView):
    model = Journal
    template_name = 'journal/journal_detail.html'


class JournalUpdateForm(LoginRequiredMixin, UpdateView):
    model = Journal
    template_name = 'journal/journal_form.html'
    form_class = JournalForm
    success_url = reverse_lazy('documents:journal_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        return context


class JournalDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Journal


class FutureListView(LoginRequiredMixin, ListView):
    model = Future
    template_name = 'future/future_list.html'


class FutureCreateView(LoginRequiredMixin, CreateView):
    model = Future
    template_name = 'future/future_form.html'
    form_class = FutureForm
    success_url = reverse_lazy('documents:future_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['future_types'] = FUTURE_TYPES
        return context


class FutureDetailsView(LoginRequiredMixin, DetailView):
    model = Future
    template_name = 'future/future_detail.html'


class FutureUpdateForm(LoginRequiredMixin, UpdateView):
    model = Future
    template_name = 'future/future_form.html'
    form_class = FutureForm
    success_url = reverse_lazy('documents:future_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resumes']=Document.objects.filter(type="Resume")
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['future_types'] = FUTURE_TYPES
        return context


class FutureDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Future


class CoWorkListView(LoginRequiredMixin, ListView):
    model = CoWork
    template_name = 'cowork/cowork_list.html'


class CoWorkCreateView(LoginRequiredMixin, CreateView):
    model = CoWork
    template_name = 'cowork/cowork_form.html'
    form_class = CoWorkForm
    success_url = reverse_lazy('documents:cowork_list')
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        # context['fields'] = DOCUMENT_FIELDS
        context['cowork_types'] = COWORK_TYPES
        context['person_types'] = PERSON_TYPES
        return context


class CoWorkDetailsView(LoginRequiredMixin, DetailView):
    model = CoWork
    template_name = 'cowork/cowork_detail.html'


class CoWorkUpdateForm(LoginRequiredMixin, UpdateView):
    model = CoWork
    template_name = 'cowork/cowork_form.html'
    form_class = CoWorkForm
    success_url = reverse_lazy('documents:cowork_list')
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers']= Center.objects.all()
        # context['fields']=DOCUMENT_FIELDS
        context['cowork_types'] = COWORK_TYPES
        context['person_types'] = PERSON_TYPES
        return context


class CoWorkDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = CoWork


class CoreListView(LoginRequiredMixin, ListView):
    model = Core
    template_name = 'core/core_list.html'


class CoreCreateView(LoginRequiredMixin, CreateView):
    model = Core
    template_name = 'core/core_form.html'
    form_class = CoreForm
    success_url = reverse_lazy('documents:core_list')
    extra_context = {
        'title': 'create',
    }


class CoreDetailsView(LoginRequiredMixin, DetailView):
    model = Core
    template_name = 'core/core_detail.html'


class CoreUpdateForm(LoginRequiredMixin, UpdateView):
    model = Core
    template_name = 'core/core_form.html'
    form_class = CoreForm
    success_url = reverse_lazy('documents:core_list')
    extra_context = {
        'title': 'update',
    }


class CoreDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Core


class TechListView(LoginRequiredMixin, ListView):
    model = Tech
    template_name = 'tech/tech_list.html'


class TechCreateView(LoginRequiredMixin, CreateView):
    model = Tech
    template_name = 'tech/tech_form.html'
    form_class = TechForm
    success_url = reverse_lazy('documents:tech_list')
    extra_context = {
        'title': 'create',
    }


class TechDetailsView(LoginRequiredMixin, DetailView):
    model = Tech
    template_name = 'tech/tech_detail.html'


class TechUpdateForm(LoginRequiredMixin, UpdateView):
    model = Tech
    template_name = 'tech/tech_form.html'
    form_class = TechForm
    success_url = reverse_lazy('documents:tech_list')
    extra_context = {
        'title': 'update',
    }


class TechDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Tech


class CompanyListView(LoginRequiredMixin, ListView):
    model = Company
    template_name = 'company/company_list.html'


class CompanyCreateView(LoginRequiredMixin, CreateView):
    model = Company
    template_name = 'company/company_form.html'
    form_class = CompanyForm
    success_url = reverse_lazy('documents:company_list')
    extra_context = {
        'title': 'create',
    }


class CompanyDetailsView(LoginRequiredMixin, DetailView):
    model = Company
    template_name = 'company/company_detail.html'


class CompanyUpdateForm(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = 'company/company_form.html'
    form_class = CompanyForm
    success_url = reverse_lazy('documents:company_list')
    extra_context = {
        'title': 'update',
    }


class CompanyDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Company


class CenterPersonnelCreateView(LoginRequiredMixin, CreateView):
    model = CenterPersonnel
    template_name = 'center_personnel/center_personnel_form.html'
    form_class = CenterPersonnelForm
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['center_pk']=self.kwargs['center_pk']
        return context

    def get_success_url(self):
        doc=CenterData.objects.get(id=self.kwargs['center_pk'])
        if doc.type == 'Core':
            return reverse_lazy('documents:core_details', kwargs={'pk': self.kwargs['center_pk']})
        elif doc.type == 'TechUnit':
            return reverse_lazy('documents:tech_details', kwargs={'pk': self.kwargs['center_pk']})
        elif doc.type == 'Company':
            return reverse_lazy('documents:company_details', kwargs={'pk': self.kwargs['center_pk']})


class CenterPersonnelUpdateForm(LoginRequiredMixin, UpdateView):
    model = CenterPersonnel
    template_name = 'center_personnel/center_personnel_form.html'
    form_class = CenterPersonnelForm
    extra_context = {
        'title': 'update',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['center_pk']=self.kwargs['center_pk']
        return context

    def get_success_url(self):
        doc=CenterData.objects.get(id=self.kwargs['center_pk'])
        if doc.type == 'Core':
            return reverse_lazy('documents:core_details', kwargs={'pk': self.kwargs['center_pk']})
        elif doc.type == 'TechUnit':
            return reverse_lazy('documents:tech_details', kwargs={'pk': self.kwargs['center_pk']})
        elif doc.type == 'Company':
            return reverse_lazy('documents:company_details', kwargs={'pk': self.kwargs['center_pk']})


class CenterPersonnelDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = CenterPersonnel


class CenterProjectCreateView(LoginRequiredMixin, CreateView):
    model = CenterProject
    template_name = 'center_project/center_project_form.html'
    form_class = CenterProjectForm
    extra_context = {
        'title': 'create',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['center_pk']=self.kwargs['center_pk']
        context['levels']=CENTERPROJECT_LEVELS
        return context

    def get_success_url(self):
        doc=CenterData.objects.get(id=self.kwargs['center_pk'])
        if doc.type == 'Core':
            return reverse_lazy('documents:core_details', kwargs={'pk': self.kwargs['center_pk']})
        elif doc.type == 'TechUnit':
            return reverse_lazy('documents:tech_details', kwargs={'pk': self.kwargs['center_pk']})
        elif doc.type == 'Company':
            return reverse_lazy('documents:company_details', kwargs={'pk': self.kwargs['center_pk']})


class CenterProjectUpdateForm(LoginRequiredMixin, UpdateView):
    model = CenterProject
    template_name = 'center_project/center_project_form.html'
    form_class = CenterProjectForm
    extra_context = {
        'title': 'update',
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['center_pk']=self.kwargs['center_pk']
        context['levels']=CENTERPROJECT_LEVELS
        return context

    def get_success_url(self):
        doc=CenterData.objects.get(id=self.kwargs['center_pk'])
        if doc.type == 'Core':
            return reverse_lazy('documents:core_details', kwargs={'pk': self.kwargs['center_pk']})
        elif doc.type == 'TechUnit':
            return reverse_lazy('documents:tech_details', kwargs={'pk': self.kwargs['center_pk']})
        elif doc.type == 'Company':
            return reverse_lazy('documents:company_details', kwargs={'pk': self.kwargs['center_pk']})




class CenterProjectDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = CenterProject


class AjaxHandler(TemplateView):
    def get(self, request, *args, **kwargs):
        request_type = request.GET.get('request_type')
        data = {'error': 0}

        if request_type == 'profile_password_change':
            profile_id = request.GET.get('profile_id')
            new_password = request.GET.get('new_password')
            profile = Profile.objects.get(id=profile_id)
            profile.user.set_password(new_password)
            profile.user.save()

        if request_type == 'delete_attachment':
            attachment_id = request.GET.get('attachment_id')
            try:
                attachemnt = DocumentAttachment.objects.get(id=attachment_id)
                attachemnt.delete()
            except:
                data = {'error': 1}

        return JsonResponse(data)
