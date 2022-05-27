
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
        else:
            pass


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
        context['centers'] = CENTER_LIST
        context['types'] = ARTICLE_PUBLISH_TYPES
        context['levels'] = ARTICLE_PUBLISH_LEVELS
        context['fields'] = DOCUMENT_FIELDS
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
        context['centers']=CENTER_LIST
        context['types']=ARTICLE_PUBLISH_TYPES
        context['levels']=ARTICLE_PUBLISH_LEVELS
        context['fields']=DOCUMENT_FIELDS
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
        context['centers'] = CENTER_LIST
        context['fields'] = DOCUMENT_FIELDS
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
        context['centers']=CENTER_LIST
        context['fields']=DOCUMENT_FIELDS
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
        context['centers'] = CENTER_LIST
        context['fields'] = DOCUMENT_FIELDS
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
        context['centers']=CENTER_LIST
        context['fields']=DOCUMENT_FIELDS
        return context


class ExperienceDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Experience


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
        context['centers']=CENTER_LIST
        return context


class ResumeDetailsView(LoginRequiredMixin, DetailView):
    model = Resume
    template_name = 'resume/resume_detail.html'


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
        context['centers'] = CENTER_LIST
        return context


class ResumeDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Resume


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
