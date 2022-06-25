from modeltranslation.translator import translator, TranslationOptions
from .models import Theme, MasterClass


class ThemeTranslationOptions(TranslationOptions):
    fields = ('title',)


class MasterClassTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'overview', 'duration')


translator.register(Theme, ThemeTranslationOptions)
translator.register(MasterClass, MasterClassTranslationOptions)
