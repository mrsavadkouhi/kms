from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
	# Security
	path('check-file-access-permission/<path:request_path_uri>', MediaFileAccessController.as_view(), name='media_access_control'),

	path('profile/list', ProfileListView.as_view(), name='profile_list'),
	path('profile/add', ProfileCreateView.as_view(), name='profile_create'),
	path('profile/<pk>', ProfileDetailsView.as_view(), name='profile_details'),
	path('profile/edit/<pk>', ProfileUpdateView.as_view(), name='profile_update'),
	path('profile/delete/<pk>', ProfileDeleteView.as_view(), name='profile_delete'),
]
