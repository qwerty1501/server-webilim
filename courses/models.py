from random import choice
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist
# from multiselectfield import MultiSelectField
from django.contrib.auth import get_user_model
from user.models import Mentor
from .fields import OrderField
from django.contrib.contenttypes.fields import GenericRelation
from courses.choices import COURSE_FORMAT, ONLINE


User = get_user_model()


class CourseCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория курса'
        verbose_name_plural = 'Категории курсов'


class Course(models.Model):
    category = models.ForeignKey(
        CourseCategory, related_name='courses', on_delete=models.CASCADE, 
        verbose_name="Категория", null=True, blank=True
    )
    mentor = models.ForeignKey(
        Mentor, related_name='courses_created', on_delete=models.CASCADE, 
        verbose_name="Куратор"
    )
    title = models.CharField(max_length=200, verbose_name="Название")
    subtitle = models.CharField(
        max_length=200, verbose_name='Подзаголовок', null=True, blank=True
    )
    overview = models.TextField(verbose_name="Описание курса"
    )
    image = models.ImageField(
        upload_to='courses/', verbose_name='Изображение', blank=True, null=True
    )
    video = models.URLField(verbose_name='Видео', blank=True, null=True)
    learning_topics = models.TextField(verbose_name='На курсе вы научитесь...')
    schedule = models.CharField(
        max_length=200, verbose_name='График проведения'
    )
    duration_months = models.CharField(
        max_length=200, verbose_name='Длительность в месяцах'
    )
    format = models.PositiveSmallIntegerField(
        choices=COURSE_FORMAT, verbose_name='Формат проведения курса', default=ONLINE
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ('-created',)

    def __str__(self):
        return self.title


class CourseReview(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='reviews'
    )
    text = models.TextField(verbose_name='Отзыв')
    video = models.URLField(verbose_name='Видео')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ('-created',)

    def __str__(self):
        if self.video:
            return self.video
        return f'{self.text[:20]}...'


class Module(models.Model):
    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE, verbose_name='Курс'
    )
    title = models.CharField(max_length=200, verbose_name='Модуль')
    order = OrderField(blank=True, for_fields=[
                       'course'], verbose_name='Порядок')

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        verbose_name = "Модуль"
        verbose_name_plural = "Модули"
        ordering = ('order',)


class Lesson(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name='lessons', verbose_name='Модуль'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    order = OrderField(blank=True, for_fields=[
                       'module'], verbose_name='Порядок')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        return f'Урок: {self.title}/Module: {self.module.title}/Course: {self.module.course.title}'

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ('order',)


class Content(models.Model):
    lesson = models.ForeignKey(
        Lesson, related_name='contents', on_delete=models.CASCADE, verbose_name='Урок'
    )
    order = OrderField(blank=True, for_fields=[
                       'lesson'], verbose_name='Порядок')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'Модуль: {self.lesson.module}, Урок: {self.lesson.title} Курс: {self.lesson.module.course}'

    class Meta:
        verbose_name = "Контент"
        verbose_name_plural = "Контенты"
        ordering = ('order',)


class ItemBase(models.Model):
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    contents = GenericRelation(Content)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    body = models.TextField()

    def __str__(self):
        return f'Текст: {self.title}'

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"
        ordering = ('-created',)


class File(ItemBase):
    file = models.FileField(upload_to='files')

    def __str__(self):
        return f'Файл: {self.title}'

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"
        ordering = ('-created',)


class Image(ItemBase):
    file = models.FileField(upload_to='images')

    def __str__(self):
        return f'Изображение: {self.title}'

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"
        ordering = ('-created',)


class Video(ItemBase):
    url = models.URLField()

    def __str__(self):
        return f'Видео: {self.title}'

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
        ordering = ('-created',)


class CourseComment(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='course_comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user_comments'
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )
    likes = models.ManyToManyField(
        User, related_name='liked_comments', blank=True, 
        verbose_name='Пользователи, которым нравится комментарий'
    )
    total_likes = models.PositiveIntegerField(
        default=0, verbose_name='Кол-во лайков', db_index=True,
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        if self.author.username:
            return f'Автор: {self.author.username}, Комментарий: {self.text}'
        return f'Автор: {self.author.email}, Комментарий: {self.text}'
    
    class Meta:
        verbose_name = 'Курс/Комментарий'
        verbose_name_plural = 'Курс/Комментарии'


class CommentReply(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор'
    )
    comment = models.ForeignKey(
        CourseComment, on_delete=models.CASCADE, verbose_name='Коммент', related_name='replies'
    )
    text = models.TextField(
        verbose_name='Ответ на комментарий'
    )
    likes = models.ManyToManyField(
        User, related_name='liked_replies', blank=True, 
        verbose_name='Пользователи, которым нравится ответ на комментарий'
    )
    total_likes = models.PositiveIntegerField(
        default=0, verbose_name='Кол-во лайков', db_index=True,
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    def __str__(self):
        if self.author.username:
            return f'Автор: {self.author.username}, Ответ на комментарий: {self.text}'
        return f'Автор: {self.author.email}, Ответ на комментарий: {self.text}'

    class Meta:
        verbose_name = 'Курс/Ответ на комментарий'
        verbose_name_plural = 'Курс/Ответы на комментарии'


class FAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
    question = models.CharField(verbose_name='Вопрос', max_length=255)
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question


class CourseFAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ Курса'
        verbose_name_plural = 'FAQ Курсов'
    question = models.CharField(verbose_name='Вопрос', max_length=255)
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question


class ArticleFAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ Статьи'
        verbose_name_plural = 'FAQ Статьи'
    question = models.CharField(verbose_name='Вопрос', max_length=255)
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question


class TravelFAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ Путешествия'
        verbose_name_plural = 'FAQ Путешествий'
    question = models.CharField(verbose_name='Вопрос', max_length=255)
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question


class MasterclassFAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ Мастер-Класса'
        verbose_name_plural = 'FAQ Мастер-Классов'
    question = models.CharField(verbose_name='Вопрос', max_length=255)
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question


class WebinarFAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ Вебинара'
        verbose_name_plural = 'FAQ Вебинаров'
    question = models.CharField(verbose_name='Вопрос', max_length=255)
    answer = models.TextField(verbose_name='Ответ')

    def __str__(self):
        return self.question


class CourseProgress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.JSONField(default='{}')
