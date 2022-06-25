from rest_framework import viewsets
from .models import MasterClass
from rest_framework import generics
from .serializers import MasterClassListSerialier, MasterClassDetailSerialier
from rest_framework import filters as drf_filters
from django_filters import rest_framework as filters
from .pagination import StandardResultsSetPagination


class ClassViewset(viewsets.ReadOnlyModelViewSet):
    pass
    # queryset = MasterClass.objects.all()
    # serializer_class = MasterClassSerialier

    # filter_backends = [
    #     filters.DjangoFilterBackend,
    #     rest_filters.SearchFilter
    # ]
    # filter_fields = ['title']
    # search_fields = ['title', 'id']


class MasterClassListView(generics.ListAPIView):
    queryset = MasterClass.objects.all()
    serializer_class = MasterClassListSerialier
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('themes',)
    pagination_class = StandardResultsSetPagination


class MasterClassDetailView(generics.RetrieveAPIView):
    queryset = MasterClass.objects.all()
    serializer_class = MasterClassDetailSerialier
