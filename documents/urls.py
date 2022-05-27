from django.urls import path

from .views import *

app_name = 'documents'

urlpatterns = [
	path('attachment/<pk>/add', DocumentAttachmentCreateView.as_view(), name='attach_create'),

	path('', ArticleListView.as_view(), name='home'),

	path('article/list', ArticleListView.as_view(), name='article_list'),
	path('article/add', ArticleCreateView.as_view(), name='article_create'),
	path('article/<pk>', ArticleDetailsView.as_view(), name='article_details'),
	path('article/edit/<pk>', ArticleUpdateForm.as_view(), name='article_update'),
	path('article/delete/<pk>', ArticleDeleteView.as_view(), name='article_delete'),

	path('resume/list', ResumeListView.as_view(), name='resume_list'),
	path('resume/add', ResumeCreateView.as_view(), name='resume_create'),
	path('resume/<pk>', ResumeDetailsView.as_view(), name='resume_details'),
	path('resume/edit/<pk>', ResumeUpdateForm.as_view(), name='resume_update'),
	path('resume/delete/<pk>', ResumeDeleteView.as_view(), name='resume_delete'),

	path('ajax/', AjaxHandler.as_view(), name='ajax'),
]
