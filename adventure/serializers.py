from rest_framework import serializers
from .models import (
    Peculiarity, Travel, TravelParticipant, TravelReview, TravelCategory, TravelProgram
)
from user.serializers import MentorSerializer


class TravelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        fields = ['id', 'mentor', 'category', 'title_ru', 'title_ky', 'subtitle_ru', 'subtitle_ky', 'image', 'start_date', 
                'end_date', 'description_ru', 'description_ky', 'duration', 'concept_for_travel_ru', 
                'concept_for_travel_ky', 'new', 'sold_out', 'seats', 'created']


class TravelProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelProgram
        fields = ['title_ru', 'title_ky', 'body_ru', 'body_ky', 'start_date', 'day']


class TravelParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelParticipant
        fields = ['adventure', 'full_name', 'phone', 'email']


class TravelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelCategory
        fields = ['title_ru', 'title_ky']


class TravelReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelReview
        fields = ['text', 'video']


class PecularitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Peculiarity
        fields = ['title_ru', 'title_ky', 'description_ru', 'description_ky', 'image']


class TravelDetailSerializer(serializers.ModelSerializer):
    mentor = MentorSerializer(read_only=True,)
    category = TravelCategorySerializer(read_only=True,)
    reviews = TravelReviewSerializer(read_only=True, many=True)
    days = TravelProgramSerializer(read_only=True, many=True)
    peculiarities = PecularitySerializer(read_only=True, many=True)
    seats_left = serializers.CharField(source='get_seats_left')
    class Meta:
        model = Travel
        fields = ['mentor', 'category', 'title_ru', 'title_ky', 'image', 'image2', 'image3', 'video', 'subtitle_ru', 'subtitle_ky', 'start_date', 'end_date',
                'description_ru', 'description_ky', 'duration', 'concept_for_travel_ru', 'concept_for_travel_ky', 'new', 'sold_out', 'seats', 'seats_left', 'peculiarities', 'days', 'reviews']
