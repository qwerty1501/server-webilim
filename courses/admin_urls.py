from django.urls import path
from . import admin_views


urlpatterns = [
     # delete 
    path('lesson/<int:lesson_id>/content/<int:id>/delete/',
         admin_views.ContentDeleteView.as_view(),
         name='lesson_content_delete'),

     # list module/lesson/content 
    path('<int:course_id>/module/<int:module_id>/', 
         admin_views.ModuleContentListView.as_view(), name='content-list-module'),
    path('<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/', 
         admin_views.ModuleContentListView.as_view(), name='content-list-lesson'),

     # manage content
    path('lesson/<int:lesson_id>/content/<model_name>/create/',
         admin_views.ContentCreateUpdateView.as_view(),
         name='lesson_content_create'),
    path('lesson/<int:lesson_id>/content/<model_name>/<id>/',
         admin_views.ContentCreateUpdateView.as_view(),
         name='lesson_content_update'),

     # order module/lesson/content
    path('module/order/',
         admin_views.ModuleOrderView.as_view(),
         name='module_order'),
    path('lesson/order/',
         admin_views.LessonOrderView.as_view(),
         name='lesson_order'),
    path('content/order/',
         admin_views.ContentOrderView.as_view(),
         name='content_order'),
]
