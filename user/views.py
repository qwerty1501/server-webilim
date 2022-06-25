from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, HelpInChoosing, Mentor
from .serializers import (
    RegisterSerializer, HelpInChoosingSerializer, MentorSerializer, RegisterRequestSerializer,
    UserProfileSerializer, ChangePasswordSerializer, MembershipDetailSerializer, TokenRefreshSerializer,
    TokenObtainSerializer, ForgotPasswordSerializer, ForgotPassCompleteSerializer, MailingSerializer,
    UserMembershipDetailSerializer, RgObject, UserPaymentsInfoSerializer
)
from rest_framework import generics
from rest_framework import viewsets
from membership.models import Coupon, RegisterRequest
from rest_framework import status
from membership.payment import *
from membership.models import RegisterRequest, RegisterRequestPayment
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from .utils import send_activation_code, get_subscription_period
from django.utils import timezone


class RegisterView(APIView):

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            obj = serializer.save()
            obj.set_password(obj.activation_code)

            #TODO promo code required for now, no technical task provided
            if obj.promo_code:
                coupon = get_object_or_404(Coupon, code=obj.promo_code)
                price = coupon.get_price_with_coupon()
                payment_data = get_url(user_data=obj, course=True, discount_price=price)
            # else:
            #     payment_data = get_url(user_data=obj, course=True)
            return Response(
                {'user':serializer.data, 'payment_data': payment_data}, 201
            )


class ActivationView(APIView):

    def get(self, request, email, activation_code):
        user = CustomUser.objects.filter(
            email=email,
            activation_code=activation_code
        ).first()
        msg_ = (
            "User does not exist",
            "Activated!"
        )
        if not user:
            return Response(msg_, 400)
        user.activation_code = ''
        user.is_active = True
        user.save()
        return Response(msg_[-1], 200)


class HelpInChoosingView(generics.CreateAPIView):
    queryset = HelpInChoosing.objects.all()
    serializer_class = HelpInChoosingSerializer


class MentorViewset(viewsets.ReadOnlyModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class RegisterRequestView(generics.CreateAPIView):
    queryset = RegisterRequest.objects.all()
    serializer_class = RegisterRequestSerializer

    def perform_create(self, serializer):
        user_data = serializer.save()
        if user_data.promo_code != '':
            coupon = get_object_or_404(Coupon, code=user_data.promo_code)
            price = coupon.get_price_with_coupon()
            payment_data = get_url(user_data=user_data, discount_price=price)
        else:
            payment_data = get_url(user_data=user_data)
        return json.dumps(payment_data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'register-request-data': serializer.data, 'payment-data': payment_data}, status=status.HTTP_201_CREATED, headers=headers)


class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMembershipDetaiView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserMembershipDetailSerializer


class CustomGetTokenView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer


class CustomRefreshTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class ForgotPasswordView(APIView):

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()
            return Response(
                "Reset code was sent to your email!", 200
            )


class ForgotPasswordConfirmView(APIView):
    def post(self, request):
        serializer = ForgotPassCompleteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                "Your password was successfully updated!", 200
            )


class MailingSubView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = MailingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.subscribe_for_mailing()
            return Response('Subscribed successfully!')


class SuccessfullPayment(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        rg_data = RgObject(data=request.data)
        if rg_data.is_valid(raise_exception=True):
            import datetime
            todays_date = datetime.date.today()
            rg = get_object_or_404(RegisterRequest, id=rg_data.validated_data.get('register_request'))
            end_date = get_subscription_period(rg.type, todays_date)
            rg.is_paid = 1
            rg.paid_date = todays_date
            rg.expire_date = end_date
            rg.save()
            # create payments for rg
            rg_payment = RegisterRequestPayment.objects.create(
                register_request=rg, paid_date=todays_date, expire_date=end_date, 
                type=rg.type, paid_price=rg.paid_price, is_paid=1
            )
            data = {
                'register_request':rg_payment.register_request.id, 
                'paid_date': rg_payment.paid_date, 'expire_date': rg_payment.expire_date, 'type':rg_payment.type, 
                'paid_price': rg_payment.paid_price, 'is_paid': rg_payment.is_paid
            }
            return Response(data)


class UserPayments(generics.RetrieveAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = CustomUser.objects.all()
    serializer_class = UserPaymentsInfoSerializer


class RegisterCourseView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterRequestSerializer

    def perform_create(self, serializer):
        user_data = serializer.save()
        if user_data.promo_code != '':
            coupon = get_object_or_404(Coupon, code=user_data.promo_code)
            price = coupon.get_price_with_coupon()
            print(price)
            payment_data = get_url(user_data, discount_price=price)
        else:
            payment_data = get_url(user_data)
        return json.dumps(payment_data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'register-request-data': serializer.data, 'payment-data': payment_data}, status=status.HTTP_201_CREATED, headers=headers)
