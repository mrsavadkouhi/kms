from django.urls import path

from .views import *

app_name = 'documents'

urlpatterns = [
	path('article/list', ArticleListView.as_view(), name='article_list'),
	path('article/add', ArticleCreateView.as_view(), name='article_create'),
	path('article/<pk>/', ArticleDetailsView.as_view(), name='article_details'),
	path('article/<pk>/edit', ArticleUpdateForm.as_view(), name='article_update'),
	path('article/delete/<pk>', ArticleDeleteView.as_view(), name='article_delete'),

	path('book/list', BookListView.as_view(), name='book_list'),
	path('book/add', BookCreateView.as_view(), name='book_create'),
	path('book/<pk>/', BookDetailsView.as_view(), name='book_details'),
	path('book/<pk>/edit', BookUpdateForm.as_view(), name='book_update'),
	path('book/delete/<pk>', BookDeleteView.as_view(), name='book_delete'),

	path('ajax/', AjaxHandler.as_view(), name='ajax'),
]
