from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import News, Email
from .utils import mailing_for_news


@receiver(post_save, sender=News)
def send_news_email(sender, instance, **kwargs):
    emails = [object.user.email for object in Email.objects.all()]
    title, description = instance.title, instance.description
    mailing_for_news(emails, title, description)
