from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, \
    DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from .models import Course, Module, Content, Lesson
from .forms import ModuleFormSet


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'admin/courses/content_list.html'

    def get(self, request, course_id, module_id, lesson_id=None):
        lesson = None
        course = get_object_or_404(Course, id=course_id)
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course=course)
        if lesson_id:
            lesson = get_object_or_404(Lesson, id=lesson_id, module=module)
        return self.render_to_response({'module': module, 'lesson': lesson})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'admin/courses/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, lesson_id, model_name, id=None):
        self.lesson = get_object_or_404(Lesson,
                                        id=lesson_id
                                        )
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id)
        return super().dispatch(request, lesson_id, model_name, id)

    def get(self, request, lesson_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, lesson_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.owner = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(lesson=self.lesson,
                                       item=obj)
            return redirect(
                'content-list-lesson', self.lesson.module.course.id,
                self.lesson.module.id, self.lesson.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id, lesson_id):

        lesson = get_object_or_404(Lesson, id=lesson_id)
        content = get_object_or_404(Content,
                                    id=id,
                                    lesson=lesson)
        content.item.delete()
        content.delete()
        return redirect(
            'content-list-lesson', content.lesson.module.course.id,
            content.lesson.module.id, content.lesson.id)


class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class LessonOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    def post(self, request):
        for id, order in self.request_json.items():
            Lesson.objects.filter(id=id).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id).update(order=order)
        return self.render_json_response({'saved': 'OK'})
