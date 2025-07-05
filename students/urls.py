from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/update/', views.update_student, name='update_student'),
    path('bulk-promote/', views.bulk_promote_students, name='bulk_promote_students'),
    path('reviewers/', views.reviewers_list, name='reviewers_list'),
    path('reviewers/assign/', views.assign_reviewer, name='assign_reviewer'),
    path('reviewers/<int:pk>/remove/', views.remove_reviewer, name='remove_reviewer'),
    path('my-profile/', views.my_student_profile, name='my_student_profile'),
]
