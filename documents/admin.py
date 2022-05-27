from django.contrib import admin
from .models import *


@admin.register(DocumentAttachment)
class DocumentAttachmentAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['file', 'description']
	list_display = ['file', 'description']
	search_fields = ['file', 'description']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code']
	list_display = ['title', 'organization_code']
	search_fields = ['title', 'organization_code']


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'entrance_year']
	list_display = ['title', 'organization_code', 'entrance_year']
	search_fields = ['title', 'organization_code', 'entrance_year']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'producer']
	list_display = ['title', 'organization_code', 'producer']
	search_fields = ['title', 'organization_code', 'producer']
