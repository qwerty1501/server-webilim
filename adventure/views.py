from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import viewsets
from .serializers import (
    TravelListSerializer, TravelParticipantSerializer, TravelCategorySerializer, TravelDetailSerializer
)
from rest_framework.decorators import action
from rest_framework import filters as drf_filters
from django_filters import rest_framework as filters
# from .permissions import IsEnrolled
from django.utils import timezone
import datetime


class TravelParticipantView(generics.CreateAPIView):
    queryset = TravelParticipant.objects.all()
    serializer_class = TravelParticipantSerializer


class TravelListView(generics.ListAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category',)


class TravelDetailView(generics.RetrieveAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelDetailSerializer


class TravelListComingView(generics.ListAPIView):
    queryset = Travel.objects.all()
    serializer_class = TravelListSerializer

    def list(self, request, *args, **kwargs):
        now = datetime.datetime.now()
        queryset = self.get_queryset().filter(start_date__gte=now)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TravelViewSet(viewsets.ViewSet):
    pass
#     filter_backends = (filters.DjangoFilterBackend,)
#     filterset_fields = ('category', 'new', 'sold_out')


#     def filter_queryset(self, queryset):
#         filter_backends = (filters.DjangoFilterBackend, )
#     # Other condition for different filter backend goes here
#         for backend in list(filter_backends):
#             queryset = backend().filter_queryset(self.request, queryset, view=self)
#         return queryset

#     def list(self, request):
#         queryset = Travel.objects.all()
#         serializer = TravelListSerializer(self.filter_queryset(queryset), many=True, context={"request": request})
#         # serializer = TravelListSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Travel.objects.all()
#         travel = get_object_or_404(queryset, pk=pk)
#         serializer = TravelDetailSerializer(travel)
#         return Response(serializer.data)
