from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from modeltranslation.admin import TranslationAdmin
from .models import (
    Travel, TravelParticipant, TravelProgram, Peculiarity, TravelCategory,
    TravelReview
)

class TravelForm(forms.ModelForm):
    description_ru = forms.CharField(widget=CKEditorWidget(), label='Про путешествие: [ru]')
    description_ky = forms.CharField(widget=CKEditorWidget(), label='Про путешествие: [ky]')
    concept_for_travel_ru = forms.CharField(widget=CKEditorWidget(), label='Концепция путешествия: [ru]')
    concept_for_travel_ky = forms.CharField(widget=CKEditorWidget(), label='Концепция путешествия: [ky]')
    class Meta:
        model = Travel
        fields = ['mentor', 'title', 'category', 'subtitle', 'image', 'start_date', 'end_date', 'new', 'sold_out', 'description', 'duration', 'concept_for_travel', 'seats']


class TravelCategoryAdmin(TranslationAdmin):
    class Meta:
        model = TravelCategory
        fields = ['title']


class TravelProgramAdmin(TranslationAdmin):
    list_display = ['adventure', 'title', 'day']
    list_filter = ['adventure', 'day', 'start_date']
    search_fields = ['title', 'body']


class TravelAdmin(TranslationAdmin):
    form = TravelForm
    list_display = ['mentor', 'title', 'category', 'new', 'sold_out', 'duration']
    list_filter = ['mentor', 'created', 'seats', 'new', 'sold_out', 'duration']
    search_fields = ['title', 'description']


class TravelParticipantAdmin(admin.ModelAdmin):
    list_display = ['adventure', 'full_name', 'phone', 'email']
    list_filter = ['adventure',]
    search_fields = ['full_name', 'phone', 'email']


class PeculiarityAdmin(TranslationAdmin):
    list_display = ['title', 'description']
    list_filter = ['travel',]
    search_fields = ['title', 'description']


class TravelReviewAdmin(admin.ModelAdmin):
    list_display = ['travel', 'video']
    list_filter = ['travel', 'created']
    search_fields = ['text']


admin.site.register(Travel, TravelAdmin)
admin.site.register(TravelCategory, TravelCategoryAdmin)
admin.site.register(TravelParticipant, TravelParticipantAdmin)
admin.site.register(TravelProgram, TravelProgramAdmin)
admin.site.register(Peculiarity, PeculiarityAdmin)
admin.site.register(TravelReview, TravelReviewAdmin)
