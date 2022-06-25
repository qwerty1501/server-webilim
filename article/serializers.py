from rest_framework import serializers
from .models import Article, ArticleComment, ArticleCommentReply
from user.models import CustomUser, Mentor
from courses.serializers import CommentAuthorSerializer


class ArticleCommentReplySerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer(read_only=True)
    class Meta:
        model = ArticleCommentReply
        fields = ('author', 'comment', 'text', 'likes', 'total_likes', 'created')


class ArticleCommentSerializer(serializers.ModelSerializer):
    article_comment_replies = ArticleCommentReplySerializer(many=True, read_only=True)
    author = CommentAuthorSerializer(read_only=True)

    class Meta:
        model = ArticleComment
        fields = ('id', 'author', 'text', 'likes', 'total_likes', 'article_comment_replies', 'created')


class ArticleMentorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mentor
        fields = ('full_name', 'image', 'short_bio')


class ArticleListSerializer(serializers.ModelSerializer):
    author = ArticleMentorSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ['id', "title", 'author', 'subtitle', 'created_at', 'new']


class ArticleDetailSerializer(serializers.ModelSerializer):
    article_comments = ArticleCommentSerializer(many=True, read_only=True)
    author = ArticleMentorSerializer(read_only=True)
    class Meta:
        model = Article
        fields = ['title', 'author', 'subtitle', 'description', 'image', 'video', 'created_at', 'article_comments']


class CreateArticleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleComment
        fields = ('article', 'author', 'text')


class CreateArticleReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleCommentReply
        fields = ('author', 'comment', 'text')
