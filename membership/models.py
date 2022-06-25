from django.db import models
from django.forms import BooleanField, ValidationError
# from user.models import CustomUser as User
from membership.choices import MONTH, SUBSCRIPTION, PACKAGE
from masterclass.models import MasterClass
from courses.models import Course
from webinar.models import Webinar
from django.core.validators import MinValueValidator, MaxValueValidator
import random
import secrets
from decimal import Decimal
from article.models import Article
from django.contrib.auth import get_user_model
User = get_user_model()


class CourseMembership(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='memberships',
        verbose_name='Курс'
    )
    membership_type = models.PositiveSmallIntegerField(
        choices=SUBSCRIPTION, default=MONTH, verbose_name='Тип подписки'
    )
    price = models.DecimalField(
        default=0, verbose_name='Цена',
        max_digits=9, decimal_places=2
    )

    def __str__(self):
        return f'Курс: {self.course}, Тип подписки: {self.get_membership_type_display()}'

    class Meta:
        verbose_name = 'Пакет курса'
        verbose_name_plural = 'Пакеты курсов'


class UserMembership(models.Model):
    user = models.OneToOneField(
        User, related_name='user_membership', verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    course_membership = models.ForeignKey(
        CourseMembership,
        on_delete=models.SET_NULL, null=True, verbose_name='Подписка на курс', blank=True
    )
    register_request = models.OneToOneField(
        'RegisterRequest', on_delete=models.PROTECT, verbose_name='Форма заявки', 
        null=True, blank=True, related_name='rg_membership'
    )
    active = models.BooleanField(
        default=False, verbose_name='Активный?'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата подписки'
    )

    def __str__(self):
        if self.course_membership:
            return f'Студент: {self.user.email}, Тип подписки на курс: \
                {self.course_membership.get_membership_type_display()}'
        return f'Студент: {self.user.email}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Package(models.Model):
    title = models.CharField(
        verbose_name='Заголовок/Тип Оплаты', max_length=255
    )
    description = models.TextField(
        'Описание/Состав пакета'
    )
    price = models.DecimalField(
        default=0, verbose_name='Цена',
        max_digits=9, decimal_places=2
    )
    type = models.PositiveSmallIntegerField(
        choices=PACKAGE, default=MONTH, verbose_name='Тип пакета'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Создан'
    )

    def __str__(self):
        return f'Пакет: {self.get_type_display()}, Описание:{self.title}'

    class Meta:
        verbose_name = 'Пакет'
        verbose_name_plural = 'Пакеты'


class RegisterRequest(models.Model):
    class SUBSCRIPTION_STATUS(models.TextChoices):
        USED = 'used', 'used',
        EXPIRED = 'expired', 'expired'
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    email = models.EmailField(
        max_length=200, verbose_name='Почта', unique=True)
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата заявки'
    )
    promo_code = models.CharField(
        verbose_name='Промокод', max_length=50, blank=True)
    package_membership = models.ForeignKey(
        Package, on_delete=models.PROTECT, verbose_name='Пакет')
    payment_url = models.URLField(
        verbose_name='Ссылка оплаты', blank=True, null=True)
    payment_id = models.CharField(
        verbose_name='ID оплаты', blank=True, null=True, max_length=255)


    #TODO: paste fields into UserMembership model
    # fill after payment  
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено?")

    # membership fields
    type = models.CharField(
        verbose_name='Тип пакета', null=True, blank=True, max_length=255,
    )
    paid_price = models.CharField(
        verbose_name='Конечная сумма', max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=32,
        verbose_name='Статус подписки',
        choices=SUBSCRIPTION_STATUS.choices,
        default=SUBSCRIPTION_STATUS.USED,
    )
    # fill after payment  
    expire_date = models.DateField(
        verbose_name='Срок истечения', null=True, blank=True)
    paid_date = models.DateField(
        verbose_name='Дата покупки', null=True, blank=True)

    def __str__(self):
        return f'Заявка на подписку: {self.email}'

    class Meta:
        verbose_name = 'Заявка на регистрацию'
        verbose_name_plural = 'Заявки на регистрации'

    def save(self, *args, **kwargs):
        if not self.type:
            self.type = self.package_membership.get_type_display()
        super().save(*args, **kwargs)


class CoursePackage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, verbose_name='Пакет', related_name='base_compound'
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name='Курс', 
    )

    def __str__(self):
        return f'{self.id}, Курс: {self.course.title}'


class MasterClassPackage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, verbose_name='Пакет',
    )
    masterclass = models.ForeignKey(
        MasterClass, on_delete=models.CASCADE, verbose_name='Мастер-Класс', 
    )

    def __str__(self):
        return f'{self.id}, Мастер-Класс: {self.masterclass.title}'


class WebinarPackage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, verbose_name='Пакет', 
    )
    webinar = models.ForeignKey(
        Webinar, on_delete=models.CASCADE, verbose_name='Вебинар',
    )

    def __str__(self):
        return f'{self.id}, Вебинар: {self.webinar.title}'


class ArticlePackage(models.Model):
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, verbose_name='Пакет',
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='Статья', 
    )

    def __str__(self):
        return f'{self.id}, Статья: {self.article.title}'


class Coupon(models.Model):
    package = models.ForeignKey(
        Package, verbose_name='Пакет', on_delete=models.CASCADE, related_name='coupons'
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        verbose_name='Купон/Промокод',
        help_text='Поле не обязательное, если оставить пустым код сгенерируется автоматически'
    )
    valid_from = models.DateTimeField(
        verbose_name='Действует от'
    )
    valid_to = models.DateTimeField(
        verbose_name='Действует до'
    )
    discount = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)],
        verbose_name='Скидка в процентах'
    )
    final_price = models.DecimalField(
        default=0, verbose_name='Цена со скидкой',
        max_digits=9, decimal_places=2,
        help_text='Заполняется автоматически после сохранения',
        blank=True
    )
    active = models.BooleanField(default=True, verbose_name='Активный')

    def __str__(self):
        return f'Пакет: {self.package.type} Купон/Промокод: {self.code}'

    def get_price_with_coupon(self):
        discount = self.discount / Decimal('100') * self.package.price
        return self.package.price - discount

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def clean(self):
        if self.valid_from > self.valid_to:
            raise ValidationError(
                f'Дата "Действует от" не может быть больше "Действует до"!')

    def save(self, *args, **kwargs):
        if not self.code:
            upper_alpha = "ABCDEFGHJKLMNPQRSTVWXYZ"
            random_str = "".join(secrets.choice(upper_alpha) for i in range(8))
            self.code = (random_str + str(random.randint(0, 10)))[-8:]
        if not self.final_price:
            discount = self.discount / Decimal('100') * self.package.price
            self.final_price = self.package.price - discount
        super().save(*args, **kwargs)


class RegisterRequestPayment(models.Model):
    register_request = models.ForeignKey(
        RegisterRequest, on_delete=models.CASCADE, verbose_name='Заявка на регистрацию', related_name='rg_payments'
    )
    paid_date = models.DateField(
    verbose_name='Дата покупки', null=True, blank=True)
    expire_date = models.DateField(
    verbose_name='Срок истечения', null=True, blank=True)
    type = models.CharField(max_length=255, verbose_name='Тип пакета/Описание')
    paid_price = models.CharField(
        verbose_name='Конечная сумма', max_length=255, null=True, blank=True)
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')

    def __str__(self):
        # if self.register_request.rg_membership:
        #     return f'Пользователь: {self.register_request.rg_membership.user.email} Пакет: {self.type}'
        return f'paid object: {self.id}'

    class Meta:
        verbose_name = 'Оплата пользователя'
        verbose_name_plural = 'Оплаты пользователей'
