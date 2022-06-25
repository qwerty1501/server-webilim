from modeltranslation.translator import translator, TranslationOptions
from .models import Course, Module, Lesson, FAQ


class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'duration_months',  'overview', 'learning_topics', 'schedule')


class ModuleTranslationOptions(TranslationOptions):
    fields = ('title',)


class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


translator.register(Module, ModuleTranslationOptions)
translator.register(Course, CourseTranslationOptions)
translator.register(FAQ, FAQTranslationOptions)
