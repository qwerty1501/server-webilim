from django.contrib import admin
from .models import Article, ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    list_fields = ['title', 'subtitle',
                   'description' 'image', 'video', 'new']
    list_filter = ['author']
    search_fields = ['title']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment)
