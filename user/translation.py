from modeltranslation.translator import translator, TranslationOptions
from .models import Mentor


class MentorTranslationOptions(TranslationOptions):
    fields = ('short_bio', 'bio')


translator.register(Mentor, MentorTranslationOptions)
