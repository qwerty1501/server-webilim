from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from .permissions import IsEnrolled
from .serializers import (
    CourseWithContentsSerializer, CourseListSerializer, CourseDetailSerializer,
    FAQListSerializer, ModuleListSerializer, LessonContentSerializer, CreateCourseCommentSerializer,
    CreateCourseReplyCommentSerializer, UserCommentsSerializer, CourseCommentsSerializer,
    CourseCategorySerializer, CourseFAQSerializer, ArticleFAQSerializer, TravelFAQSerializer,
    WebinarFAQSerializer, MasterclassFAQSerializer, FreeCourseDetailSerializer, FreeCourseDetailSerializerWrapper,
    BoughtCourseDetailSerializerWrapper, CourseProgressSerializer
)
from user.models import CustomUser
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveAPIView
from courses.utils import get_membership
from rest_framework import status
from rest_framework.exceptions import APIException,ParseError,NotFound
from django_filters.rest_framework import DjangoFilterBackend
import json
# class CourseViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseDetailSerializer

#     @action(detail=True, methods=['post'],
#             authentication_classes=[BasicAuthentication],
#             permission_classes=[IsAuthenticated], )
#     def enroll(self, request, *args, **kwargs):
#         course = self.get_object()
#         course.students.add(request.user)
#         return Response({'enrolled': True})

#     @action(detail=True, methods=['get'],
#             serializer_class=CourseWithContentsSerializer,
#             authentication_classes=[BasicAuthentication],
#             permission_classes=[IsAuthenticated, IsEnrolled])
#     def contents(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['format', 'category',]


class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        is_bought = get_membership(self.request.user, instance)
        if is_bought:
            instance = {'bought': instance}
            serializer = BoughtCourseDetailSerializerWrapper(instance)
            return Response(serializer.data)
        else:
            # FreeCourseDetailSerializerWrapper
            instance = {'free': instance}
            serializer = FreeCourseDetailSerializerWrapper(instance)
            return Response(serializer.data)


class FAQListView(generics.ListAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQListSerializer


class ModuleListView(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleListSerializer

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        return self.queryset.filter(course=course)


class LessonsContentsView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonContentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        module = course.modules.filter(id=self.kwargs.get('module_id')).first()
        return self.queryset.filter(module=module)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        course = get_object_or_404(Course, id=self.kwargs.get('course_id'))
        is_bought = get_membership(self.request.user, course)
        if is_bought:
            return Response(serializer.data)
        else:
            raise APIException('Course was not bought!')


class AddCourseComment(generics.CreateAPIView):
    queryset = CourseComment.objects.all()
    serializer_class = CreateCourseCommentSerializer


class AddCourseReplyComment(generics.CreateAPIView):
    queryset = CommentReply.objects.all()
    serializer_class = CreateCourseReplyCommentSerializer


class UserCourseCommentsView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCommentsSerializer


class UserCourseCommentsUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = CourseComment.objects.all()
    serializer_class = CourseCommentsSerializer


class CourseCategoryList(generics.ListAPIView):
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

# /////////
class CourseFAQListView(generics.ListAPIView):
    queryset = CourseFAQ.objects.all()
    serializer_class = CourseFAQSerializer


class ArticleFAQListView(generics.ListAPIView):
    queryset = ArticleFAQ.objects.all()
    serializer_class = ArticleFAQSerializer


class MasterclassFAQListView(generics.ListAPIView):
    queryset = MasterclassFAQ.objects.all()
    serializer_class = MasterclassFAQSerializer


class TraveFAQListView(generics.ListAPIView):
    queryset = TravelFAQ.objects.all()
    serializer_class = TravelFAQSerializer


class WebinarFAQListView(generics.ListAPIView):
    queryset = WebinarFAQ.objects.all()
    serializer_class = WebinarFAQSerializer


class CourseProgressView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('course'))
        cp, _ = CourseProgress.objects.\
            get_or_create(course=course, user=request.user)
        serializer = CourseProgressSerializer(cp)
        return Response(serializer.data)


class CourseProgressAddView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        course = get_object_or_404(Course, pk=kwargs.get('course'))
        cp, _ = CourseProgress.objects.\
            get_or_create(course=course, user=request.user)
        module_id = next(iter(request.data))

        if not isinstance(module_id, str) or not isinstance(request.data[module_id], str):
            return Response('Data should be in string!', status=status.HTTP_400_BAD_REQUEST)

        # first time updating field from default
        if isinstance(cp.data, str):
            cp.data = {module_id:[request.data[module_id]]}
            cp.save()
            serializer = CourseProgressSerializer(cp)
            return Response(serializer.data)

        if module_id in cp.data:
            if request.data[module_id] not in cp.data[module_id]:
                cp.data[module_id].append(request.data[module_id])
                cp.save()
            else:
                return Response(f'{request.data[module_id]} already marked as passed!', status=status.HTTP_400_BAD_REQUEST)
        else:
            cp.data[module_id] = [request.data[module_id]]
            cp.save()
        serializer = CourseProgressSerializer(cp)
        return Response(serializer.data)
