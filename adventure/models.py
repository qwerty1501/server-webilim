from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import timedelta
from django.utils import timezone
from user.models import Mentor


User = get_user_model()


class TravelCategory(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Категория путешествия'
        verbose_name_plural = 'Категории путешествий'


class Travel(models.Model):
    mentor = models.ForeignKey(Mentor, verbose_name="Куратор", related_name='created_adventures', on_delete=models.CASCADE)
    category = models.ForeignKey(TravelCategory, verbose_name='Категория', null=True, on_delete=models.CASCADE, related_name='travels')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    image = models.ImageField(upload_to='travels/', verbose_name='Изображение', null=True, blank=True)
    image2 = models.ImageField(upload_to='travels/', verbose_name='Изображение', null=True, blank=True)
    image3 = models.ImageField(upload_to='travels/', verbose_name='Изображение', null=True, blank=True)
    video = models.URLField(verbose_name='Видео', null=True, blank=True)
    subtitle = models.CharField(max_length=200, verbose_name='Подзаголовок', null=True, blank=True)
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    description = models.TextField(verbose_name='Про путешествие')
    duration = models.PositiveIntegerField(verbose_name='Продолжительность в днях', default=1, validators=[MinValueValidator(1), MaxValueValidator(100)])
    concept_for_travel = models.TextField(verbose_name='Концепция путешествия')
    new = models.BooleanField(default=True, verbose_name='Новое')
    sold_out = models.BooleanField(default=False, verbose_name='Расспродан')
    week = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    seats = models.PositiveIntegerField(default=0, verbose_name='Кол-во мест')

    def save(self, *args, **kwargs):
        if not self.week:
            self.week = timezone.now() + timedelta(days=7)
        # if self.travel_participants.count >= self.seats:
        #     self.sold_out = True
        super(Travel, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Путешествие'
        verbose_name_plural = 'Путешествия'
        ordering = ('-created',)

    def get_seats_left(self):
        seats_left = self.seats - self.travel_participants.count()
        return f'Количество свободных мест: {seats_left} Заполнено: {self.travel_participants.count()}'


class TravelProgram(models.Model):
    adventure = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='days', verbose_name='Путешествие')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Описание')
    start_date = models.DateField(verbose_name='Дата начала')
    day = models.PositiveIntegerField(verbose_name='День', default=1)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Программа Путешествия'
        verbose_name_plural = 'Программы Путешествий'
        ordering = ('day',)


class TravelParticipant(models.Model):
    adventure = models.ForeignKey(Travel, on_delete=models.CASCADE, verbose_name='Путешествие', related_name='travel_participants')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Почта')


    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = 'Участник путешествия'
        verbose_name_plural = 'Участники путешествий'


class Peculiarity(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, related_name='peculiarities', verbose_name='Путешествие')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='travel_peculiarity')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Особенность и Эмоция'
        verbose_name_plural = 'Особенности и Эмоции'


class TravelReview(models.Model):
    travel = models.ForeignKey(Travel, on_delete=models.CASCADE, verbose_name='Путешествие', related_name='reviews')
    text = models.TextField(verbose_name='Отзыв')
    video = models.URLField(verbose_name='Видео')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Отзыв про путешествие"
        verbose_name_plural = "Отзывы про путешествия"
        ordering = ('-created',)

    def __str__(self):
        if self.video:
            return self.video
        return f'{self.text[:20]}...'
