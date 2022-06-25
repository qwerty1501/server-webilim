from django.urls import path
from . import views


urlpatterns = [
    # path('<int:id>/<slug:slug>/', views.package_detail, name='package_detail'),
    path('get_payment_url/', views.GetPaymentUrlView.as_view(), name='get_payment_url'),
    path('package-list/', views.PackageListView.as_view(), name='package_list'),
    path('promo-code-check/', views.PromoCodeCheckView.as_view(), name='promo_code_check'),
]
