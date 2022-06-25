from modeltranslation.translator import translator, TranslationOptions
from .models import Travel, TravelProgram, Peculiarity, TravelCategory


class TravelCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


class TravelTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description', 'concept_for_travel')


class TravelProgramTranslationOptions(TranslationOptions):
    fields = ('title', 'body')


class PeculiarityTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


translator.register(Peculiarity, PeculiarityTranslationOptions)
translator.register(TravelProgram, TravelProgramTranslationOptions)
translator.register(Travel, TravelTranslationOptions)
translator.register(TravelCategory, TravelCategoryTranslationOptions)
