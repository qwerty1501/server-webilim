from django.contrib import admin
from django import forms
from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget
from user.models import (
    CustomManager, CustomUser, HelpInChoosing, Mentor, CompanyReview, News, Email
)
from membership.models import UserMembership
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = CustomUser
        fields = '__all__'

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
            user.save()
        return user


class MentorForm(forms.ModelForm):
    short_bio_ru = forms.CharField(widget=CKEditorWidget(), label='Короткая биография: [ru]')
    short_bio_ky = forms.CharField(widget=CKEditorWidget(), label='Короткая биография: [ky]')
    bio_ru = forms.CharField(widget=CKEditorWidget(), label='Биография: [ru]')
    bio_ky = forms.CharField(widget=CKEditorWidget(), label='Биография: [ky]')
    class Meta:
        model = Mentor
        fields = ['full_name', 'short_bio', 'bio', 'image', ]


class MentorAdmin(TranslationAdmin):
    form = MentorForm
    list_display = ['full_name', 'short_bio', 'image']


class HelpInChoosingAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'email']
    list_filter = ['created']
    search_fields = ['full_name', 'phone', 'email']


class CompanyReviewAdmin(admin.ModelAdmin):
    list_display = ['video']
    list_filter = ['created']
    search_fields = ['text']


class UserMembershipInline(admin.StackedInline):
    model = UserMembership


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ['email', 'full_name', 'phone', 'is_student', 'is_active']
    list_filter = ['is_student', 'is_active']
    search_fields = ['email']
    inlines = [UserMembershipInline]
    # readonly_fields = ['full_name']

    def full_name(self, obj):
        return obj.full_name
    full_name.empty_value_display = 'NULL'


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title' , 'description', 'created')
    search_fields = ('title',)
    list_filter = ('created',)


class EmailsAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, UserAdmin)
admin.site.register(Mentor, MentorAdmin)
admin.site.register(HelpInChoosing, HelpInChoosingAdmin)
admin.site.register(CompanyReview, CompanyReviewAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Email, EmailsAdmin)
