from django.urls import path
from masterclass import views


urlpatterns = [
    path('master-classes/', views.MasterClassListView.as_view(), name='master-classes'),
    path('master-classes/<int:pk>/', views.MasterClassDetailView.as_view(), name='master-class'),
]
