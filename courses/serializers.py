from rest_framework import serializers

# from margulaninfo.user.models import CustomUser
from user.models import CustomUser
from .models import *
from user.serializers import MentorSerializer
from membership.models import CourseMembership


class TravelFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelFAQ
        fields = ('question', 'answer')


class ArticleFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleFAQ
        fields = ('question', 'answer')


class CourseFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFAQ
        fields = ('question', 'answer')


class MasterclassFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterclassFAQ
        fields = ('question', 'answer')


class WebinarFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarFAQ
        fields = ('question', 'answer')

# -----------------------------------------------------------------

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['title', 'body']


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'url']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'file']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['title', 'file']


class ItemRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, Image):
            serializer = ImageSerializer(value, context=self.context)
        elif isinstance(value, Video):
            serializer = VideoSerializer(value)
        elif isinstance(value, Text):
            serializer = TextSerializer(value)
        elif isinstance(value, File):
            serializer = FileSerializer(value, context=self.context)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data


class ContentSerializer(serializers.ModelSerializer):
    item = ItemRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = ('item', )


# without content serializer
class LessonsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'order')


class LessonSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)

    class Meta:
        model = Lesson
        fields = ('id', 'module', 'title', 'order', 'contents')


class FreeLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'module', 'title', 'order',)

class FreeModuleSerializer(serializers.ModelSerializer):
    lessons = FreeLessonSerializer(many=True)

    class Meta:
        model = Module
        fields = ('title', 'lessons')

class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Module
        fields = ('title', 'lessons')


class CourseWithContentsSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True)
    mentor = MentorSerializer(read_only=True,)

    class Meta:
        model = Course
        fields = ('id', 'title', 'overview', 'created', 'mentor', 'modules')

# //////////////////////////////////////////////////////////////////////////


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMembership
        fields = (
            'membership_type', 'price'
        )


class CourserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseReview
        fields = ('text', 'video')


# class ModuleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Module
#         fields = ('title_ru', 'title_ky', 'description_ru', 'description_ky')

class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'avatar')


class CourseCommentReplySerializer(serializers.ModelSerializer):
    author = CommentAuthorSerializer(read_only=True)
    class Meta:
        model = CommentReply
        fields = ('author', 'comment', 'text', 'likes', 'total_likes', 'created')


class CourseCommentSerializer(serializers.ModelSerializer):
    replies = CourseCommentReplySerializer(many=True, read_only=True)
    author = CommentAuthorSerializer(read_only=True)

    class Meta:
        model = CourseComment
        fields = ('id', 'author', 'text', 'likes', 'total_likes', 'replies', 'created')


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'title']


class FreeCourseDetailSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)
    modules = FreeModuleSerializer(many=True, read_only=True)
    mentor = MentorSerializer(read_only=True,)
    reviews = CourserReviewSerializer(read_only=True, many=True)
    course_comments = CourseCommentSerializer(many=True, read_only=True)
    memberships = MembershipSerializer(many=True, read_only=True)
    format = serializers.CharField(source='get_format_display')

    class Meta:
        model = Course
        fields = (
            'id', 'category', 'mentor', 'title_ru', 'title_ky', 'subtitle_ru',
            'subtitle_ky', 'image', 'format', 'video', 'overview_ru', 'overview_ky',
            'schedule_ru', 'schedule_ky', 'learning_topics_ru', 'learning_topics_ky',
            'duration_months_ru', 'duration_months_ky', 'memberships', 'modules', 'reviews',
            'course_comments'
        )

class FreeCourseDetailSerializerWrapper(serializers.ModelSerializer):
    free = FreeCourseDetailSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ('free',)

class CourseDetailSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    mentor = MentorSerializer(read_only=True,)
    reviews = CourserReviewSerializer(read_only=True, many=True)
    course_comments = CourseCommentSerializer(many=True, read_only=True)
    memberships = MembershipSerializer(many=True, read_only=True)
    format = serializers.CharField(source='get_format_display')

    class Meta:
        model = Course
        fields = (
            'id', 'category', 'mentor', 'format', 'title_ru', 'title_ky', 'subtitle_ru',
            'subtitle_ky', 'image', 'video', 'overview_ru', 'overview_ky',
            'schedule_ru', 'schedule_ky', 'learning_topics_ru', 'learning_topics_ky',
            'duration_months_ru', 'duration_months_ky', 'memberships', 'modules', 'reviews',
            'course_comments'
        )

class BoughtCourseDetailSerializerWrapper(serializers.ModelSerializer):
    bought = CourseDetailSerializer(read_only=True)
    class Meta:
        model = Course
        fields = ('bought',)


class CourseListSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)
    category = CourseCategorySerializer(read_only=True)
    format = serializers.CharField(source='get_format_display')
    class Meta:
        model = Course
        fields = (
            'id','category', 'mentor', 'title_ru', 'title_ky', 'format', 'subtitle_ru', 'subtitle_ky', 'image', 'video',
            'overview_ru', 'overview_ky', 'schedule_ru', 'schedule_ky', 'learning_topics_ru',
            'learning_topics_ky', 'created', 'modules'
        )


class FAQListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ('question_ru', 'question_ky', 'answer_ru', 'answer_ky')


class ModuleListSerializer(serializers.ModelSerializer):
    lessons = LessonsListSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ('course', 'order', 'title', 'lessons')


class LessonContentSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'order', 'contents')


class CreateCourseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseComment
        fields = ('course', 'author', 'text')


class CreateCourseReplyCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = ('author', 'comment', 'text')


class CourseCommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseComment
        fields = ('id', 'text', 'created')


class UserCommentsSerializer(serializers.ModelSerializer):
    user_comments = CourseCommentsSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = ('user_comments', 'full_name')


class CourseProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseProgress
        fields = ('course', 'user', 'data')
