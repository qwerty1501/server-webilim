from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

from .views import (
    RegisterView, ActivationView, HelpInChoosingView, RegisterRequestView,
    UserProfileUpdateView, ChangePasswordView, UserMembershipDetaiView,
    CustomGetTokenView, CustomRefreshTokenView, ForgotPasswordView, ForgotPasswordConfirmView,
    MailingSubView, SuccessfullPayment, UserPayments
)

urlpatterns = [
     # user sign up and password conf
    path('register/', RegisterView.as_view()),
    path('forgot-password/confirm/', ForgotPasswordConfirmView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
  
    path('activate/<str:email>/<str:activation_code>/',
         ActivationView.as_view(), name='activate'),

     # login
    path('login/', CustomGetTokenView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomRefreshTokenView.as_view(), name='token_refresh'),

     # request forms
    path('register-request/', RegisterRequestView.as_view(),
         name='register_request'),
    path('create-help-in-choosing/', HelpInChoosingView.as_view(),
         name='create_help_in_choosing'),
    path('mailing-sub/', MailingSubView.as_view()),

    # user profile
    path('user-profile/<int:pk>/',
         UserProfileUpdateView.as_view(), name='user-profile'),
    path('user-payments/<int:pk>/',
         UserPayments.as_view(), name='user-payments'),
    path('change-password/',
         ChangePasswordView.as_view(), name='change-password'),
    path('user-membership/<int:pk>/',
         UserMembershipDetaiView.as_view(), name='user-membership'),

    # after payment requests
    path('after-reqister-request-payment/', SuccessfullPayment.as_view(), name='after-pay') 
]
