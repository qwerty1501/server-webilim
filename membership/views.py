from rest_framework.views import APIView
from .payment import *
from django.conf import settings
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from membership.models import Package, RegisterRequest
from membership.serializers import PackageListSerializer, PromoCodeCheckSerializer
from rest_framework.exceptions import NotFound
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone


class GetPaymentUrlView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PackageListView(generics.ListAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageListSerializer


class PromoCodeCheckView(APIView):
    queryset = RegisterRequest.objects.all()
    serializer_class = PromoCodeCheckSerializer

    def post(self, request, format=None):
        now = timezone.localtime()
        package_id = request.data.get('package_membership')
        code = request.data.get('promo_code')
        if not package_id or not code:
            raise ValidationError({"message":"Not valid code or package id!"})
        try:
            package = Package.objects.get(id=package_id)
        except Package.DoesNotExist:
            raise ValidationError({"Package does not exist!"})
        coupon = package.coupons.filter(
            code=code, valid_from__lte=now, valid_to__gte=now, active=True)\
            .first()
        if not coupon:
            raise NotFound('Invalid coupon code!')
        return Response({"data": request.data, "price_with_promocod": coupon.final_price}, status=status.HTTP_200_OK)
