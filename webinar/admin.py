from django.contrib import admin
from .models import Webinar, WebinarCategory, WebinarReview
from django import forms 
from ckeditor.widgets import CKEditorWidget
from modeltranslation.admin import TranslationAdmin


class WebinarForm(forms.ModelForm):
    overview_ru = forms.CharField(widget=CKEditorWidget(), label='Описание: [ru]')
    overview_ky = forms.CharField(widget=CKEditorWidget(), label='Описание: [ky]')
    class Meta:
        model = Webinar
        fields = ['mentor', 'category', 'title', 'subtitle', 'video', 
            'image', 'video', 'overview', 'new', 'start_date', 'duration']


@admin.register(WebinarCategory)
class WebinarCategoryAdmin(TranslationAdmin):
    list_display = ['title']
    search_fields = ['title']
    # prepopulated_fields = {'slug': ('title',)}


@admin.register(Webinar)
class WebinarAdmin(TranslationAdmin):
    form = WebinarForm
    list_display = ['title', 'created']
    list_filter = ['created',]
    search_fields = ['title', 'overview']


@admin.register(WebinarReview)
class WebinarReviewAdmin(admin.ModelAdmin):
    list_display = ['video']
    list_filter = ['created']
    search_fields = ['text']
