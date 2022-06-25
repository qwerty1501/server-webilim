from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

# from membership.models import Coupon
# from payments.models import BasePayment


class CustomManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            msg_ = ("Email not provided!")
            raise ValueError(msg_)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            msq_ = ('Email not provided!')
            raise ValueError(msq_)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    class Gender(models.TextChoices):
        MALE = 'male', 'male',
        FEMALE = 'female', 'female'

    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')
    full_name = models.CharField(
        verbose_name='Полное имя', max_length=200, blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=50)
    is_student = models.BooleanField(verbose_name='Студент?', default=False)
    avatar = models.ImageField(
        upload_to='avatars/', verbose_name='Аватар', null=True, blank=True
    )
    is_active = models.BooleanField(default=False, verbose_name='Активный')
    activation_code = models.CharField(
        max_length=25, blank=True, verbose_name='Код для активации'
    )
    company = models.CharField(
        verbose_name='Название компании/Род деятельности', max_length=255, blank=True, null=True
    )
    date_of_birth = models.DateField(
        verbose_name='Дата рождения',  blank=True, null=True
    )
    gender = models.CharField(
        max_length=32,
        verbose_name='Пол',
        choices=Gender.choices,
        default=Gender.MALE,
    )

    # additional fields
    country = models.CharField(
        max_length=255, verbose_name='Страна', null=True, blank=True
    )
    city = models.CharField(
        max_length=255, verbose_name='Город', null=True, blank=True
    )
    occupation = models.CharField(
        max_length=255, verbose_name='Род деятельности', null=True, blank=True
    )
    expertise = models.CharField(
        max_length=255, verbose_name='Экспертиза', null=True, blank=True
    )
    timezone = models.CharField(
        max_length=255, verbose_name='Часовой пояс', null=True, blank=True
    )
    web_site = models.CharField(
        max_length=255, verbose_name='Веб-сайт', null=True, blank=True
    )
    expertise_description = models.TextField(
        verbose_name='Чем вы занимаетесь?', null=True, blank=True
    )

    # social networks
    instagram = models.URLField(
        verbose_name='Инстаграм', blank=True, null=True
    )
    telegram = models.URLField(
        verbose_name='Телеграм', blank=True, null=True
    )
    whatsapp = models.URLField(
        verbose_name='Вотсап', blank=True, null=True
    )
    youtube = models.URLField(
        verbose_name='Ютуб', blank=True, null=True
    )
    linkedin = models.URLField(
        verbose_name='Линкедин', blank=True, null=True
    )
    promo_code = models.CharField(
        max_length=255, null=True, blank=True
    )
    objects = CustomManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self) -> str:
        return f"{self.email} -> {self.id}"

    def create_activation_code(self):
        code = get_random_string(
            length=10,
            allowed_chars='1234567890#$%!?_'
        )
        self.activation_code = code
        self.save(update_fields=['activation_code'])


class HelpInChoosing(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    email = models.EmailField(max_length=200, verbose_name='Почта')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата заявки')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Помощь в выборе'
        verbose_name_plural = 'Помощь в выборе'


class Mentor(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    image = models.ImageField(upload_to='mentors/',
                              verbose_name='Изображение', null=True)
    short_bio = models.CharField(max_length=200, verbose_name='Короткое БИО')
    bio = models.TextField(verbose_name='Биография')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Ментор'
        verbose_name_plural = 'Ментора'


class CompanyReview(models.Model):
    text = models.TextField(verbose_name='Отзыв')
    video = models.URLField(verbose_name='Видео')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Отзыв про компанию"
        verbose_name_plural = "Отзывы про компанию"
        ordering = ('-created',)

    def __str__(self):
        if self.video:
            return self.video
        return f'{self.text[:20]}...'


class News(models.Model):
    title = models.CharField(
        verbose_name='Заголовок', max_length=255
    )
    description = models.TextField('Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Email(models.Model):
    """
    for sending news to emails
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='send_emails', verbose_name='Пользователь')

    def __str__(self):
        return self.user.email
