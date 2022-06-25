from django.contrib import admin
# from courses.admin import ModuleInline
from .models import Theme, MasterClass, MasterClassReview
from ckeditor.widgets import CKEditorWidget
from django import forms
from modeltranslation.admin import TranslationAdmin


class MasterClassForm(forms.ModelForm):
    overview_ru = forms.CharField(widget=CKEditorWidget(), label='Описание: [ru]')
    overview_ky = forms.CharField(widget=CKEditorWidget(), label='Описание: [ky]')
    class Meta:
        model = MasterClass
        fields = ['mentor', 'themes', 'title', 'subtitle', 'video', 
            'image', 'overview', 'new', 'start_date', 'duration']


@admin.register(Theme)
class ThemesAdmin(TranslationAdmin):
    list_display = ['title',]


@admin.register(MasterClass)
class MasterClassAdmin(TranslationAdmin):
    form = MasterClassForm
    list_display = ['title', 'themes', 'created']
    list_filter = ['created', 'themes']
    search_fields = ['title', 'overview']
    # inlines = [ModuleInline]


@admin.register(MasterClassReview)
class MaterClassReviewAdmin(admin.ModelAdmin):
    list_display = ['masterclass', 'video']
    list_filter = ['masterclass', 'created']
    search_fields = ['text']
