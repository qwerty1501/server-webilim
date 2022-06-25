from django.urls import path
from webinar import views


urlpatterns = [
    path('webinar-detail/<int:pk>/', views.WebinarDetailView.as_view(), name='webinar-detail'),
    path('webinar-list/', views.WebinarListView.as_view(), name='webinar-list'),
]
