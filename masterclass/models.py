from django.db import models
from margulan import settings
from datetime import timedelta
from django.utils import timezone
from user.models import Mentor


class Theme(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ('title',)

    def __str__(self):
        return self.title


class MasterClass(models.Model):
    mentor = models.ForeignKey(Mentor, verbose_name="Куратор", related_name='class_created', on_delete=models.CASCADE)
    themes = models.ForeignKey(Theme, related_name='master', on_delete=models.CASCADE, verbose_name="Тема")
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
        verbose_name = "Мастер-Класс"
        verbose_name_plural = "Мастер-Классы"
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.week:
            self.week = timezone.now() + timedelta(days=7)
        super(MasterClass, self).save(*args, **kwargs)


class MasterClassReview(models.Model):
    masterclass = models.ForeignKey(MasterClass, on_delete=models.CASCADE, verbose_name='Мастер-Класс', related_name='reviews')
    text = models.TextField(verbose_name='Отзыв')
    video = models.URLField(verbose_name='Видео')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Отзыв про Мастер-Класс"
        verbose_name_plural = "Отзывы про Мастер-Классы"
        ordering = ('-created',)

    def __str__(self):
        if self.video:
            return self.video
        return f'{self.text[:20]}...'
