from django.db import models
from user.models import CustomUser as User
from datetime import timedelta
from django.utils import timezone
from user.models import Mentor


class WebinarCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория вебинара'
        verbose_name_plural = 'Категории вебинаров'


class Webinar(models.Model):
    mentor = models.ForeignKey(Mentor, verbose_name="Куратор", null=True, related_name='webinars', on_delete=models.CASCADE)
    category = models.ForeignKey(WebinarCategory, on_delete=models.CASCADE, null=True, related_name='webinars', verbose_name='Категория')
    title = models.CharField(max_length=200, verbose_name="Название")
    subtitle = models.CharField(max_length=200, verbose_name='Подзаголовок', null=True, blank=True)
    image = models.FileField(upload_to='images/', verbose_name="Изображение", blank=True, null=True)
    video = models.URLField(verbose_name="Видео", blank=True, null=True)
    overview = models.TextField(verbose_name="Описание")
    start_date = models.DateField(verbose_name='Дата начала')
    duration = models.CharField(verbose_name='Продолжительность', max_length=50)
    new = models.BooleanField(default=True, verbose_name='Новое')
    week = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Вебинар"
        verbose_name_plural = "Вебинары"
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.week:
            self.week = timezone.now() + timedelta(days=7)
        super(Webinar, self).save(*args, **kwargs)


class WebinarReview(models.Model):
    webinar = models.ForeignKey(Webinar, on_delete=models.CASCADE, verbose_name='Вебинар', related_name='reviews')
    text = models.TextField(verbose_name='Отзыв')
    video = models.URLField(verbose_name='Видео')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Отзыв про вебинар"
        verbose_name_plural = "Отзывы про вебинары"
        ordering = ('-created',)

    def __str__(self):
        if self.video:
            return self.video
        return f'{self.text[:20]}...'
