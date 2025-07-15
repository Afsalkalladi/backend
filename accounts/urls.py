from django.urls import path
from . import views
from .admin_views import AdminDashboardAPIView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    
    # Admin dashboard endpoints
    path('admin/dashboard-stats/', AdminDashboardAPIView.dashboard_stats, name='admin_dashboard_stats'),
    path('admin/students/', AdminDashboardAPIView.students_list, name='admin_students_list'),
    path('admin/teachers/pending/', AdminDashboardAPIView.pending_teachers, name='admin_pending_teachers'),
    path('admin/teachers/<int:teacher_id>/approve/', AdminDashboardAPIView.approve_teacher, name='admin_approve_teacher'),
    path('admin/teachers/<int:teacher_id>/reject/', AdminDashboardAPIView.reject_teacher, name='admin_reject_teacher'),
    path('admin/alumni/', AdminDashboardAPIView.alumni_list, name='admin_alumni_list'),
    path('admin/alumni/pending/', AdminDashboardAPIView.pending_alumni, name='admin_pending_alumni'),
    path('admin/alumni/<int:alumni_id>/approve/', AdminDashboardAPIView.approve_alumni, name='admin_approve_alumni'),
    path('admin/alumni/<int:alumni_id>/reject/', AdminDashboardAPIView.reject_alumni, name='admin_reject_alumni'),
    path('admin/tech-heads/', AdminDashboardAPIView.tech_heads_list, name='admin_tech_heads_list'),
    path('admin/users/eligible/', AdminDashboardAPIView.eligible_users, name='admin_eligible_users'),
    path('admin/tech-heads/promote/', AdminDashboardAPIView.promote_to_tech_head, name='admin_promote_tech_head'),
    path('admin/tech-heads/<int:tech_head_id>/remove/', AdminDashboardAPIView.remove_tech_head, name='admin_remove_tech_head'),
    path('admin/academic-schemes/', AdminDashboardAPIView.academic_schemes, name='admin_academic_schemes'),
    path('admin/subjects/', AdminDashboardAPIView.subjects_list, name='admin_subjects_list'),
]
