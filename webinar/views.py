from rest_framework import viewsets
from .models import Webinar
from .serializers import WebinarListSerializer, WebinarDetailSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from masterclass.pagination import StandardResultsSetPagination


class WebinarViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Webinar.objects.all()
    serializer_class = WebinarListSerializer


class WebinarListView(generics.ListAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarListSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('category',)
    pagination_class = StandardResultsSetPagination


class WebinarDetailView(generics.RetrieveAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarDetailSerializer
