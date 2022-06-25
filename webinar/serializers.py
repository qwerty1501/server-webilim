from rest_framework import serializers
from .models import Webinar, WebinarReview, WebinarCategory
from user.serializers import MentorSerializer


class WebinarCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarCategory
        fields = ['id', 'title_ru', 'title_ky']


class WebinarReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarReview
        fields = ['text', 'video']


class WebinarListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = ['id', 'category', 'mentor', 'title_ru', 'title_ky', 'subtitle_ru', 'subtitle_ky', 
                'image', 'video', 'overview_ru', 'overview_ky', 'start_date', 'duration_ru', 'duration_ky', 'new', 'created']


class WebinarDetailSerializer(serializers.ModelSerializer):
    reviews = WebinarReviewSerializer(read_only=True, many=True)
    category = WebinarCategorySerializer(read_only=True)
    mentor = MentorSerializer(read_only=True)
    class Meta:
        model = Webinar
        fields = ['id', 'category', 'mentor', 'title_ru', 'title_ky', 'subtitle_ru', 'subtitle_ky', 
                'image', 'video', 'overview_ru', 'overview_ky', 'start_date', 'duration_ru', 'duration_ky', 'new', 'reviews']
