from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.contrib.contenttypes.admin import (
    GenericTabularInline, GenericStackedInline
)
from .models import (
    Course, Module, CourseReview, Content, Lesson, Text, File,
    Image, Video, CourseComment, CommentReply, FAQ, CourseCategory,
    TravelFAQ, ArticleFAQ, CourseFAQ, MasterclassFAQ, WebinarFAQ
)
from .forms import ModuleForm, CourseForm, LessonForm, OfflineCourseProxyForm
from django.utils.safestring import mark_safe
from django.urls import reverse
from courses.choices import OFFLINE


class EditLinkToInlineObjectModule(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk])
        if instance.pk:
            return mark_safe(u'<a href="{u}">Добавить уроки</a>'.format(u=url))
        else:
            return 'Для начала добавьте модуль...'
    edit_link.short_description = 'Уроки'


class EditLinkToInlineObjectLesson(object):
    def edit_link(self, instance):
        if instance.pk:
            url = reverse('content-list-lesson',
                          args=[instance.module.course.id, instance.module.id, instance.id])
            return mark_safe(f'<a href="{url}">Добавить контент</a>')
        else:
            return 'Для начала добавьте урок...'
    edit_link.short_description = 'Контент'

# reverse("admin:coconut_transportation_swallow_add")
# def user_detail(obj):
#     url = reverse('admin_user_detail', args=[obj.id])
#     return mark_safe(f'<a href="{url}">View</a>')


class ModuleInline(EditLinkToInlineObjectModule, admin.StackedInline):
    form = ModuleForm
    model = Module
    readonly_fields = ('edit_link',)


class LessonInline(EditLinkToInlineObjectLesson, admin.StackedInline):
    form = LessonForm
    model = Lesson
    readonly_fields = ('edit_link',)


@admin.register(Course)
class CourseAdmin(TranslationAdmin):
    list_display = ['title', 'created', ]
    list_filter = ['format', 'created']
    search_fields = ['title', 'overview']
    inlines = [ModuleInline]
    form = CourseForm


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['course', 'video']
    list_filter = ['course', 'created']
    search_fields = ['text']


class ContentInline(GenericStackedInline):
    model = Content
    extra = 1


@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['title', 'body']
    list_filter = ['contents__lesson__module__course', 'contents__lesson', ]
    inlines = [ContentInline]


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
    inlines = [ContentInline]
    list_filter = ['contents__lesson__module__course', 'contents__lesson', ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']
    inlines = [ContentInline]
    list_filter = ['contents__lesson__module__course', 'contents__lesson', ]


@admin.register(File)
class TextAdmin(admin.ModelAdmin):
    list_display = ['title', 'file']
    inlines = [ContentInline]
    list_filter = ['contents__lesson__module__course', 'contents__lesson', ]


@admin.register(Module)
class ModuleAdmin(TranslationAdmin):
    list_display = ['title', 'order']
    list_filter = ['course']
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['module', 'title', 'order']
    list_filter = ['module', 'module__course']


class OfflineCourseProxy(Course):
    class Meta:
        proxy = True
        verbose_name = 'Оффлайн курс'
        verbose_name_plural = 'Оффлайн курсы'


@admin.register(OfflineCourseProxy)
class OfflineCourseProxyAdmin(admin.ModelAdmin):
    form = OfflineCourseProxyForm
    inlines = [ModuleInline]
    list_display = ['mentor', 'title']
    list_filter = ['created',]
    search_fields = ['title', 'mentor', 'overview']

    def get_queryset(self, *args, **kwargs):
        return Course.objects.filter(format=OFFLINE)


@admin.register(CourseComment)
class CourseCommentAdmin(admin.ModelAdmin):
    list_display = ['course', 'author', 'text', 'total_likes']
    list_filter = ['course', 'author']
    search_fields = ['text',]


@admin.register(CommentReply)
class CommentReplyAdmin(admin.ModelAdmin):
    list_display = ['author', 'text', 'total_likes']
    list_filter = ['comment__course', 'author']
    search_fields = ['text',]


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question']


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(TravelFAQ)
class TravelFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']


@admin.register(ArticleFAQ)
class ArticleFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']


@admin.register(CourseFAQ)
class CourseFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']


@admin.register(MasterclassFAQ)
class MasterclassFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']


@admin.register(WebinarFAQ)
class WebinarFAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']
    search_fields = ['question', 'answer']
