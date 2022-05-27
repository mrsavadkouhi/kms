from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from documents.json_mixin import *
from .forms import *
from .models import *


# ========  Media File Access Controller ========
class MediaFileAccessController(View):
    def dispatch(self, request, *args, **kwargs):
        from django.http import HttpResponse
        if not request.user.is_authenticated:
            return HttpResponse("Login Required -- 401", status=401)

        # check if the user can access this media/static file and set `user_test_result` to `True` if so
        user_test_result = True
        if not user_test_result:
            return HttpResponse("You Have No Permission To Access This Page -- 403", status=403)

        return HttpResponse("OK", status=200)


# ========  Profile ========
class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'accounts/profile_list.html'


class ProfileDetailsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile_detail.html'


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileCreateForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('accounts:profile_list')
    extra_context = {
        'title': 'create'
    }


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('accounts:profile_list')
    extra_context={
        'title': 'update'
    }


class ProfileDeleteView(LoginRequiredMixin, JSONDeleteView):
    model = Profile