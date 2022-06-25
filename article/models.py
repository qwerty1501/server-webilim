from django.db import models
from django.contrib.auth import get_user_model

from user.models import Mentor
# from model_utils.fields import StatusField
# from django.contrib.contenttypes.fields import GenericRelation


User = get_user_model()


class BasicArticleModel(models.Model):
    created_at = models.DateField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        abstract = True


class Article(BasicArticleModel):
    title = models.CharField("Заголовок", max_length=255)
    author = models.ForeignKey(Mentor, on_delete=models.SET_NULL, verbose_name='Автор', null=True, blank=True)
    subtitle = models.CharField("Подзаголовок", max_length=255, blank=True)
    description = models.TextField("Тело статьи", blank=True, null=True)
    image = models.ImageField("Изображение",upload_to='media', null=True, blank=True)
    video = models.URLField("Видео", blank=True, null=True)
    new = models.BooleanField(default=True, verbose_name='Новое?')
    
    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title


class ArticleComment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='article_comments'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user_article_comments'
    )
    text = models.TextField(
        verbose_name='Комментарий'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата добавления'
    )
    likes = models.ManyToManyField(
        User, blank=True, related_name='user_article_comment_likes',
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
        verbose_name = 'Статья/Комментарий'
        verbose_name_plural = 'Статья/Комментарии'


class ArticleCommentReply(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор', related_name='user_article_comment_replies'
    )
    comment = models.ForeignKey(
        ArticleComment, on_delete=models.CASCADE, verbose_name='Коммент', related_name='article_comment_replies'
    )
    text = models.TextField(
        verbose_name='Ответ на комментарий'
    )
    likes = models.ManyToManyField(
        User, blank=True, related_name='user_article_comment_reply_likes',
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
        verbose_name = 'Статья/Ответ на комментарий'
        verbose_name_plural = 'Статьи/Ответы на комментарии'
