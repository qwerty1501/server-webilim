from modeltranslation.translator import translator, TranslationOptions
from .models import Webinar, WebinarCategory


class WebinarCategoryTranslationOptions(TranslationOptions):
    fields = ('title', )

class WebinarTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'overview', 'duration')


translator.register(Webinar, WebinarTranslationOptions)
translator.register(WebinarCategory, WebinarCategoryTranslationOptions)
