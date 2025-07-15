from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AlumniViewSet, TeamMemberViewSet

router = DefaultRouter()
router.register(r'alumni', AlumniViewSet, basename='alumni')
router.register(r'team-members', TeamMemberViewSet, basename='team-members')

urlpatterns = router.urls
