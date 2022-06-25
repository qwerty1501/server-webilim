from django.contrib import admin
from membership.models import (
    CourseMembership, UserMembership, Package, RegisterRequest,
    CoursePackage, MasterClassPackage, WebinarPackage, Coupon, ArticlePackage, RegisterRequestPayment
)
from django.urls import reverse
from django.utils.safestring import mark_safe
from user.models import CustomUser


class CouponInline(admin.StackedInline):
    model = Coupon
    extra = 1


class ArticlePackageInline(admin.StackedInline):
    model = ArticlePackage
 

class CoursePackageInline(admin.StackedInline):
    model = CoursePackage


class MasterClassPackageInline(admin.StackedInline):
    model = MasterClassPackage


class WebinarPackageInline(admin.StackedInline):
    model = WebinarPackage


@admin.register(CourseMembership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['course', 'membership_type', 'price']
    list_filter = ['course', 'membership_type']


@admin.register(UserMembership)
class UserMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'course_membership', 'active']
    list_filter = ['user', 'course_membership', 'active']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'type']
    list_filter = ['type']
    inlines = [CoursePackageInline, WebinarPackageInline, MasterClassPackageInline, ArticlePackageInline, CouponInline]


def user_add(obj):
    url = reverse("admin:user_customuser_add")
    return mark_safe(f'<a href="{url}">Привязать пользователя</a>')


@admin.register(RegisterRequest)
class RegisterRequestAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'promo_code', user_add, 'is_paid', 'payment_url', 'payment_id', 'paid_price', 'type']
    list_filter = ['is_paid']
    search_fields = ['full_name', 'email', 'phone', 'promo_code']
    user_add.short_description = "Создать пользователя"


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['package', 'code', 'valid_from', 'valid_to', 'discount', 'active']
    list_filter = ['package', 'active']
    search_fields = ['code']


class RegisterRequestProxy(RegisterRequest):
    class Meta:
        proxy = True
        verbose_name = 'Привязать существующего пользователя'
        verbose_name_plural = 'Привязать существующих пользователей'


class UserMembershipInline(admin.StackedInline):
    model = UserMembership
    extra = 1


@admin.register(RegisterRequestProxy)
class RegisterRequestProxyAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'promo_code', 'is_paid', 'payment_url', 'payment_id', 'paid_price', 'type']
    list_filter = ['is_paid']
    search_fields = ['full_name', 'email', 'phone', 'promo_code']
    inlines = [UserMembershipInline]


@admin.register(RegisterRequestPayment)
class RegisterRequestPaymentAdmin(admin.ModelAdmin):
    list_display = ['register_request' , 'paid_date', 'expire_date', 'type', 'paid_price', 'is_paid']
    # search_fields = ['full_name', 'email', 'phone', 'promo_code']
    list_filter = ['is_paid', 'register_request']
