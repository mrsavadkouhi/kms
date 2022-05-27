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

	path('book/list', BookListView.as_view(), name='book_list'),
	path('book/add', BookCreateView.as_view(), name='book_create'),
	path('book/<pk>', BookDetailsView.as_view(), name='book_details'),
	path('book/edit/<pk>', BookUpdateForm.as_view(), name='book_update'),
	path('book/delete/<pk>', BookDeleteView.as_view(), name='book_delete'),

	path('experience/list', ExperienceListView.as_view(), name='experience_list'),
	path('experience/add', ExperienceCreateView.as_view(), name='experience_create'),
	path('experience/<pk>', ExperienceDetailsView.as_view(), name='experience_details'),
	path('experience/edit/<pk>', ExperienceUpdateForm.as_view(), name='experience_update'),
	path('experience/delete/<pk>', ExperienceDeleteView.as_view(), name='experience_delete'),

	path('idea/list', IdeaListView.as_view(), name='idea_list'),
	path('idea/add', IdeaCreateView.as_view(), name='idea_create'),
	path('idea/<pk>', IdeaDetailsView.as_view(), name='idea_details'),
	path('idea/edit/<pk>', IdeaUpdateForm.as_view(), name='idea_update'),
	path('idea/delete/<pk>', IdeaDeleteView.as_view(), name='idea_delete'),

	path('thesis/list', ThesisListView.as_view(), name='thesis_list'),
	path('thesis/add', ThesisCreateView.as_view(), name='thesis_create'),
	path('thesis/<pk>', ThesisDetailsView.as_view(), name='thesis_details'),
	path('thesis/edit/<pk>', ThesisUpdateForm.as_view(), name='thesis_update'),
	path('thesis/delete/<pk>', ThesisDeleteView.as_view(), name='thesis_delete'),

	path('seminar/list', SeminarListView.as_view(), name='seminar_list'),
	path('seminar/add', SeminarCreateView.as_view(), name='seminar_create'),
	path('seminar/<pk>', SeminarDetailsView.as_view(), name='seminar_details'),
	path('seminar/edit/<pk>', SeminarUpdateForm.as_view(), name='seminar_update'),
	path('seminar/delete/<pk>', SeminarDeleteView.as_view(), name='seminar_delete'),

	path('workshop/list', WorkshopListView.as_view(), name='workshop_list'),
	path('workshop/add', WorkshopCreateView.as_view(), name='workshop_create'),
	path('workshop/<pk>', WorkshopDetailsView.as_view(), name='workshop_details'),
	path('workshop/edit/<pk>', WorkshopUpdateForm.as_view(), name='workshop_update'),
	path('workshop/delete/<pk>', WorkshopDeleteView.as_view(), name='workshop_delete'),

	path('conference/list', ConferenceListView.as_view(), name='conference_list'),
	path('conference/add', ConferenceCreateView.as_view(), name='conference_create'),
	path('conference/<pk>', ConferenceDetailsView.as_view(), name='conference_details'),
	path('conference/edit/<pk>', ConferenceUpdateForm.as_view(), name='conference_update'),
	path('conference/delete/<pk>', ConferenceDeleteView.as_view(), name='conference_delete'),

	path('visit/list', VisitListView.as_view(), name='visit_list'),
	path('visit/add', VisitCreateView.as_view(), name='visit_create'),
	path('visit/<pk>', VisitDetailsView.as_view(), name='visit_details'),
	path('visit/edit/<pk>', VisitUpdateForm.as_view(), name='visit_update'),
	path('visit/delete/<pk>', VisitDeleteView.as_view(), name='visit_delete'),

	path('project/list', ProjectListView.as_view(), name='project_list'),
	path('project/add', ProjectCreateView.as_view(), name='project_create'),
	path('project/<pk>', ProjectDetailsView.as_view(), name='project_details'),
	path('project/edit/<pk>', ProjectUpdateForm.as_view(), name='project_update'),
	path('project/delete/<pk>', ProjectDeleteView.as_view(), name='project_delete'),

	path('report/list', ReportListView.as_view(), name='report_list'),
	path('report/add', ReportCreateView.as_view(), name='report_create'),
	path('report/<pk>', ReportDetailsView.as_view(), name='report_details'),
	path('report/edit/<pk>', ReportUpdateForm.as_view(), name='report_update'),
	path('report/delete/<pk>', ReportDeleteView.as_view(), name='report_delete'),

	path('manual/list', ManualListView.as_view(), name='manual_list'),
	path('manual/add', ManualCreateView.as_view(), name='manual_create'),
	path('manual/<pk>', ManualDetailsView.as_view(), name='manual_details'),
	path('manual/edit/<pk>', ManualUpdateForm.as_view(), name='manual_update'),
	path('manual/delete/<pk>', ManualDeleteView.as_view(), name='manual_delete'),

	path('journal/list', JournalListView.as_view(), name='journal_list'),
	path('journal/add', JournalCreateView.as_view(), name='journal_create'),
	path('journal/<pk>', JournalDetailsView.as_view(), name='journal_details'),
	path('journal/edit/<pk>', JournalUpdateForm.as_view(), name='journal_update'),
	path('journal/delete/<pk>', JournalDeleteView.as_view(), name='journal_delete'),


	path('future/list', FutureListView.as_view(), name='future_list'),
	path('future/add', FutureCreateView.as_view(), name='future_create'),
	path('future/<pk>', FutureDetailsView.as_view(), name='future_details'),
	path('future/edit/<pk>', FutureUpdateForm.as_view(), name='future_update'),
	path('future/delete/<pk>', FutureDeleteView.as_view(), name='future_delete'),


	path('cowork/list', CoWorkListView.as_view(), name='cowork_list'),
	path('cowork/add', CoWorkCreateView.as_view(), name='cowork_create'),
	path('cowork/<pk>', CoWorkDetailsView.as_view(), name='cowork_details'),
	path('cowork/edit/<pk>', CoWorkUpdateForm.as_view(), name='cowork_update'),
	path('cowork/delete/<pk>', CoWorkDeleteView.as_view(), name='cowork_delete'),

	path('ajax/', AjaxHandler.as_view(), name='ajax'),
]
