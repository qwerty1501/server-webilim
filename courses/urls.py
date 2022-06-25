from django.urls import path
from . import views


urlpatterns = [
    path('course-detail/<int:pk>/',
         views.CourseDetailView.as_view(), name='course-detail'),
    path('user-profile-comments/update/<int:pk>/',
         views.UserCourseCommentsUpdateView.as_view(), name='user-profile-comments_update'),
    path('user-profile-comments/<int:pk>/',
         views.UserCourseCommentsView.as_view(), name='user-profile-comments'),

    path('course-category-list/', views.CourseCategoryList.as_view(), name='course-category-list'),

    path('course-list/', views.CourseListView.as_view(), name='course-list'),
    path('course-progress/<int:course>/add/', views.CourseProgressAddView.as_view(), name='course_progress_add'),
    path('course-progress/<int:course>/', views.CourseProgressView.as_view(), name='course_progress'),

    path('module-list/<int:course_id>/',
         views.ModuleListView.as_view(), name='module-list'),
    path('lessons/contents/<int:course_id>/<int:module_id>/',
         views.LessonsContentsView.as_view(), name='lessons-contents'),
    
    path('faq-list/', views.FAQListView.as_view(), name='faq-list'),

    path('course-faq-list/', views.CourseFAQListView.as_view(), name='course-faq-list'),
    path('article-faq-list/', views.ArticleFAQListView.as_view(), name='article-faq-list'),
    path('masterclass-faq-list/', views.MasterclassFAQListView.as_view(), name='masterclass-faq-list'),
    path('travel-faq-list/', views.TraveFAQListView.as_view(), name='travel-faq-list'),
    path('webinar-faq-list/', views.WebinarFAQListView.as_view(), name='webinar-faq-list'),

    path('add-course-comment/', views.AddCourseComment.as_view(),
         name='add-course-comment'),
    path('add-course-reply-comment/', views.AddCourseReplyComment.as_view(),
         name='add-course-reply-comment'),
]
