from django.contrib import admin
from .models import *


@admin.register(DocumentAttachment)
class DocumentAttachmentAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['file', 'description']
	list_display = ['file', 'description']
	search_fields = ['file', 'description']


@admin.register(Center)
class CenterAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'code']
	list_display = ['title', 'code']
	search_fields = ['title', 'code']


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
	list_filter = ['title', 'organization_code']
	list_display = ['title', 'organization_code']
	search_fields = ['title', 'organization_code']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'producer']
	list_display = ['title', 'organization_code', 'producer']
	search_fields = ['title', 'organization_code', 'producer']


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'producer']
	list_display = ['title', 'organization_code', 'producer']
	search_fields = ['title', 'organization_code', 'producer']


@admin.register(Idea)
class IdeaAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'producer']
	list_display = ['title', 'organization_code', 'producer']
	search_fields = ['title', 'organization_code', 'producer']


@admin.register(Seminar)
class Seminardmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'producer']
	list_display = ['title', 'organization_code', 'producer']
	search_fields = ['title', 'organization_code', 'producer']


@admin.register(Workshop)
class Workshopdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'producer']
	list_display = ['title', 'organization_code', 'producer']
	search_fields = ['title', 'organization_code', 'producer']


@admin.register(Manual)
class Manualdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'producer']
	list_display = ['title', 'organization_code', 'producer']
	search_fields = ['title', 'organization_code', 'producer']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	save_on_top = True
	list_filter = ['title', 'organization_code', 'manager']
	list_display = ['title', 'organization_code', 'manager']
	search_fields = ['title', 'organization_code', 'manager']
