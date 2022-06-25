from django.urls import path
from adventure import views

urlpatterns = [
    path('travel-list/coming/', views.TravelListComingView.as_view(), name='travel-list-coming'),
    path('travel-detail/<int:pk>/', views.TravelDetailView.as_view(), name='travel-detail'),
    path('travel-list/', views.TravelListView.as_view(), name='travel-list'),
    path('create-travel-participant/', views.TravelParticipantView.as_view(), name='create_travel_participant'),
]
