from django import template
from courses.models import Lesson, Course
from django.utils.safestring import mark_safe
from django.urls import reverse


register = template.Library()


@register.filter
def get_object_edit_link(obj):
    return  reverse('admin:%s_%s_change' % ( 
        obj._meta.app_label,  obj._meta.model_name),  args=[obj.pk])


@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
