from cProfile import label
from urllib import request
from rest_framework import serializers

from .models import CustomUser, Email, HelpInChoosing, Mentor
from .utils import send_activation_code
from membership.models import Package, RegisterRequest, UserMembership, RegisterRequestPayment
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.core.mail import send_mail
from membership.models import Coupon
from django.utils.crypto import get_random_string


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=4, required=False, write_only=True,
    )
    promo_code = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    class Meta:
        model = CustomUser
        fields = (
            'full_name', 'phone', 'email', 'promo_code', 'password'
        )

    def validate(self, attrs):
        code = get_random_string(
            length=10,
            allowed_chars='1234567890#$%!?_'
        )
        attrs['password'] = code 
        attrs['activation_code'] = code
        promo_code = attrs.get('promo_code')
        if promo_code:
            if Coupon.objects.filter(code=promo_code).exists():
                return attrs
        elif promo_code == '' or promo_code is None:
            return attrs
        else:
            raise serializers.ValidationError('')


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден!')

        return email

    def send_verification_email(self):
        email = self.validated_data.get('email')
        user = CustomUser.objects.get(email=email)
        user.create_activation_code()
        send_mail(
            'Забыли пароль',
            f'Ваш код для изменения пароля - {user.activation_code}',
            'admin@gmail.com',
            [user.email]
        )


class ForgotPassCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=4, required=True)
    password_confirmation = serializers.CharField(min_length=4, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password')
        password2 = attrs.get('password_confirmation')
        code = attrs.get('code')
        if not CustomUser.objects.filter(email=email, activation_code=code).exists():
            raise serializers.ValidationError("Invalid confirmation code or email!")
        if password1 != password2:
            raise serializers.ValidationError("Passwords didn't match!")
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = CustomUser.objects.get(email=email)
        user.set_password(password)
        user.save()


class HelpInChoosingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpInChoosing
        fields = ['full_name', 'phone', 'email']


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['full_name', 'short_bio_ru',
                  'short_bio_ky', 'bio_ru', 'bio_ky', 'image']


class RegisterRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterRequest
        fields = ['id', 'full_name', 'phone', 'email',
                  'promo_code', 'package_membership']

    def validate(self, data):
        code = data.get('promo_code')
        if code != '':
            package = data.get('package_membership')
            now = timezone.localtime()
            coupon = package.coupons.filter(
                code=code, valid_from__lte=now, valid_to__gte=now, active=True)\
                .first()
            if not coupon:
                raise ValidationError('Invalid coupon!')
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('avatar', 'full_name', 'company', 'phone', 'date_of_birth', 'email', 'gender',
                  'country', 'occupation', 'city', 'expertise', 'timezone', 'web_site', 'expertise_description',
                  'instagram', 'telegram', 'whatsapp', 'youtube', 'linkedin')


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class MembershipDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterRequest
        fields = ('type', 'status', 'paid_price', 'expire_date')


class TokenObtainSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data


class TokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data


class MailingSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def subscribe_for_mailing(self):
        try:
            user = CustomUser.objects.get(email=self.validated_data.get('email'))
            if Email.objects.filter(user=user).exists():
                raise serializers.ValidationError('Пользователь уже подписан!')
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден!')
        else:
            Email.objects.create(user=user)


class UserMembershipSerializer(serializers.ModelSerializer):
    register_request = MembershipDetailSerializer(read_only=True)
    class Meta:
        model = UserMembership
        fields = ('register_request',)


class UserMembershipDetailSerializer(serializers.ModelSerializer):
    user_membership = UserMembershipSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('user_membership',)


class RegisterRequestAfterPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterRequestPayment
        fields = ('paid_date', 'expire_date', 'type', 'paid_price', 'is_paid')


class RgObject(serializers.Serializer):
    register_request = serializers.IntegerField(label='ID')


class RG_User_lvl_Serializer(serializers.ModelSerializer):
    rg_payments = RegisterRequestAfterPaymentSerializer(many=True, read_only=True)
    class Meta:
        model = RegisterRequest
        fields = ('rg_payments',)


class UserNestedMembershipSerializer(serializers.ModelSerializer):
    register_request = RG_User_lvl_Serializer(read_only=True)
    class Meta:
        model = UserMembership
        fields = ('register_request',)


class UserPaymentsInfoSerializer(serializers.ModelSerializer):
    user_membership = UserNestedMembershipSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ('user_membership',)


class RegisterCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('')