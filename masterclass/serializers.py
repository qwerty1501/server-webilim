from rest_framework import serializers
from .models import MasterClass, Theme, MasterClassReview
from user.serializers import MentorSerializer


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'title_ru', 'title_ky']


class MasterClassReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterClassReview
        fields = ['masterclass', 'text', 'video']


class MasterClassListSerialier(serializers.ModelSerializer):
    mentor = MentorSerializer(read_only=True,)
    themes = ThemeSerializer(read_only=True,)
    class Meta:
        model = MasterClass
        fields = ['id', 'mentor', 'themes', 'title_ru', 'title_ky', 'subtitle_ru', 'subtitle_ky', 
                'image', 'video', 'overview_ru', 'overview_ky', 'start_date', 'duration_ru', 
                'duration_ky', 'new', 'created'
                ]
    
    # def get_m_training_path(self, obj):
    #     return obj.get_training_path_display()


class MasterClassDetailSerialier(serializers.ModelSerializer):
    mentor = MentorSerializer(read_only=True,)
    themes = ThemeSerializer(read_only=True,)
    reviews = MasterClassReviewSerializer(read_only=True, many=True)
    class Meta:
        model = MasterClass
        fields = ['id', 'mentor', 'themes', 'title_ru', 'title_ky', 'subtitle_ru', 'subtitle_ky', 
                'image', 'video', 'overview_ru', 'overview_ky', 'start_date', 'duration_ru', 'duration_ky',
                'new', 'reviews'
                ]
