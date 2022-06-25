from django.urls import path
from . import views

urlpatterns = [
    path('article-list/', views.ArticleListView.as_view(),
         name='article-list'),
    path('article-detail/<int:pk>/', views.ArticleDetailView.as_view(),
         name='article-detail'),
    path('add-article-comment/', views.AddArticleComment.as_view(),
         name='add-article-comment'),
    path('add-article-reply-comment/', views.AddArticleReplyComment.as_view(),
         name='add-article-reply-comment'),
]
