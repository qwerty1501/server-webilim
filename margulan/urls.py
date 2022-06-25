from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from courses.views import CourseViewSet
from django.conf import settings
from django.conf.urls.static import static
from masterclass.views import ClassViewset
from webinar.views import WebinarViewset
from adventure.views import TravelViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.i18n import i18n_patterns
from user.views import MentorViewset


router = DefaultRouter()
# router.register('article', ArticleViewset)
# router.register('comment', CommentViewSet)
# router.register('courses', CourseViewSet)
# router.register('masterclass', ClassViewset)
# router.register('webinar', WebinarViewset)
# router.register('travel', TravelViewSet, basename='travel')
router.register('mentor', MentorViewset)


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Margulan API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('course/', include('courses.admin_urls')),
]


urlpatterns += i18n_patterns(
    path('api/v2/', include('user.urls')),
    path('api/v2/', include('masterclass.urls')),
    path('api/v2/', include(router.urls)),
    path('api/v2/', include('courses.urls')),
    path('api/v2/', include('adventure.urls')),
    path('api/v1/', include('membership.urls')),
    path('api/v1/', include('webinar.urls')),
    path('api/v1/', include('article.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
