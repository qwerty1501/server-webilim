from django import forms
from .models import Course, Module, Lesson
from ckeditor.widgets import CKEditorWidget
from django.forms.models import inlineformset_factory
from courses.choices import OFFLINE


class CourseForm(forms.ModelForm):
    overview_ru = forms.CharField(
        widget=CKEditorWidget(), label='Описание курса: [ru]')
    overview_ky = forms.CharField(
        widget=CKEditorWidget(), label='Описание курса: [ky]')
    learning_topics_ru = forms.CharField(
        widget=CKEditorWidget(), label='На курсе вы научитесь...: [ru]')
    learning_topics_ky = forms.CharField(
        widget=CKEditorWidget(), label='На курсе вы научитесь...: [ky]')

    class Meta:
        model = Course
        fields = ['category', 'mentor', 'title', 'subtitle', 'overview', 'image',
                  'video', 'learning_topics', 'format', 'schedule', 'duration_months']


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title_ru', 'title_ky', 'order']


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title',]


ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title'],
                                      extra=2,
                                      can_delete=True)


# register proxy model for translated fields
class OfflineCourseProxyForm(forms.ModelForm):
    class Meta:
        fields = [
            'mentor', 'title_ru', 'title_ky', 'subtitle_ru', 'subtitle_ky', 'duration_months_ru',
            'duration_months_ky', 'overview_ru', 'overview_ky', 'learning_topics_ru', 'learning_topics_ky',
            'schedule_ru', 'schedule_ky', 'image', 'video'
        ]

    def clean(self):
        self.instance.format = OFFLINE
        return self.cleaned_data
