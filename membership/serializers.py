from django.forms import CharField, IntegerField
from rest_framework import serializers
from membership.models import Package, RegisterRequest


class PackageListSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = Package
        fields = ['id', 'title', 'description', 'price', 'type']

    def get_type(self,obj):
        return obj.get_type_display()


class PromoCodeCheckSerializer(serializers.Serializer):
    package_membership = IntegerField(label='ID', required=True)
    promo_code = CharField(max_length=50, required=True)
