from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_list, name='events_list'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('create/', views.create_event, name='create_event'),
    path('<int:pk>/update/', views.update_event, name='update_event'),
    path('<int:pk>/delete/', views.delete_event, name='delete_event'),
    path('upcoming/', views.upcoming_events_ticker, name='upcoming_events_ticker'),
    path('my/', views.my_events, name='my_events'),
]
