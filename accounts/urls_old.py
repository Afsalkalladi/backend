from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'alumni', views.AlumniViewSet)
router.register(r'team-members', views.TeamMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]
    path('admin/tech-heads/', AdminDashboardAPIView.tech_heads_list, name='admin_tech_heads_list'),
    path('admin/users/eligible/', AdminDashboardAPIView.eligible_users, name='admin_eligible_users'),
    path('admin/tech-heads/promote/', AdminDashboardAPIView.promote_to_tech_head, name='admin_promote_tech_head'),
    path('admin/tech-heads/<int:tech_head_id>/remove/', AdminDashboardAPIView.remove_tech_head, name='admin_remove_tech_head'),
    path('admin/academic-schemes/', AdminDashboardAPIView.academic_schemes, name='admin_academic_schemes'),
    path('admin/subjects/', AdminDashboardAPIView.subjects_list, name='admin_subjects_list'),
]
