from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from academics.models import Scheme, Subject
from events.models import Event
from projects.models import Project
from students.models import Student
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

class AdminDashboardAPIView:
    """Admin dashboard API endpoints"""
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def dashboard_stats(request):
        """Get dashboard statistics"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get basic counts
        total_students = User.objects.filter(role='student').count()
        total_teachers = User.objects.filter(role='teacher').count()
        total_alumni = User.objects.filter(role='alumni').count()
        total_tech_heads = User.objects.filter(role='tech_head').count()
        
        # Pending approvals
        pending_teachers = User.objects.filter(role='teacher', is_approved=False).count()
        pending_alumni = User.objects.filter(role='alumni', is_approved=False).count()
        
        # Active content
        active_events = Event.objects.filter(is_active=True).count()
        total_projects = Project.objects.count()
        
        # Recent activity (last 7 days)
        from datetime import timedelta
        from django.utils import timezone
        week_ago = timezone.now() - timedelta(days=7)
        
        recent_registrations = User.objects.filter(date_joined__gte=week_ago).count()
        recent_projects = Project.objects.filter(created_at__gte=week_ago).count()
        
        stats = {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_alumni': total_alumni,
            'total_tech_heads': total_tech_heads,
            'pending_approvals': pending_teachers + pending_alumni,
            'active_events': active_events,
            'total_projects': total_projects,
            'recent_activity': [
                {
                    'action': 'New Registrations',
                    'count': recent_registrations,
                    'time': 'Last 7 days'
                },
                {
                    'action': 'New Projects',
                    'count': recent_projects,
                    'time': 'Last 7 days'
                },
                {
                    'action': 'Pending Approvals',
                    'count': pending_teachers + pending_alumni,
                    'time': 'Current'
                }
            ]
        }
        
        return Response(stats)
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def students_list(request):
        """Get list of all students"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        students = User.objects.filter(role='student').select_related('student')
        
        students_data = []
        for user in students:
            student_data = {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'date_joined': user.date_joined,
                'is_approved': user.is_approved,
                'is_active': user.is_active
            }
            
            # Add student profile data if exists
            if hasattr(user, 'student'):
                student_data.update({
                    'full_name': user.student.full_name,
                    'scheme': user.student.scheme,
                    'year_of_joining': user.student.year_of_joining,
                    'ongoing_semester': user.student.ongoing_semester,
                    'year_of_study': user.student.year_of_study
                })
            
            students_data.append(student_data)
        
        return Response({'students': students_data})
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def pending_teachers(request):
        """Get list of pending teacher approvals"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        teachers = User.objects.filter(role='teacher', is_approved=False)
        
        teachers_data = []
        for teacher in teachers:
            teachers_data.append({
                'id': teacher.id,
                'username': teacher.username,
                'first_name': teacher.first_name,
                'last_name': teacher.last_name,
                'email': teacher.email,
                'date_joined': teacher.date_joined,
                'is_active': teacher.is_active
            })
        
        return Response({'pending_teachers': teachers_data})
    
    @staticmethod
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def approve_teacher(request, teacher_id):
        """Approve a teacher"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            teacher = User.objects.get(id=teacher_id, role='teacher')
            teacher.is_approved = True
            teacher.is_staff = True
            teacher.save()
            
            return Response({'message': 'Teacher approved successfully'})
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def reject_teacher(request, teacher_id):
        """Reject a teacher"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            teacher = User.objects.get(id=teacher_id, role='teacher')
            teacher.delete()
            
            return Response({'message': 'Teacher rejected and removed'})
        except User.DoesNotExist:
            return Response({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def pending_alumni(request):
        """Get list of pending alumni approvals"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        alumni = User.objects.filter(role='alumni', is_approved=False)
        
        alumni_data = []
        for alumnus in alumni:
            alumni_data.append({
                'id': alumnus.id,
                'username': alumnus.username,
                'first_name': alumnus.first_name,
                'last_name': alumnus.last_name,
                'email': alumnus.email,
                'date_joined': alumnus.date_joined,
                'is_active': alumnus.is_active
            })
        
        return Response({'pending_alumni': alumni_data})
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def alumni_list(request):
        """Get list of all alumni"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        alumni = User.objects.filter(role='alumni')
        
        alumni_data = []
        for alumnus in alumni:
            alumni_data.append({
                'id': alumnus.id,
                'username': alumnus.username,
                'first_name': alumnus.first_name,
                'last_name': alumnus.last_name,
                'email': alumnus.email,
                'date_joined': alumnus.date_joined,
                'is_approved': alumnus.is_approved,
                'is_active': alumnus.is_active
            })
        
        return Response({'alumni': alumni_data})

    @staticmethod
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def approve_alumni(request, alumni_id):
        """Approve an alumni"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            alumni = User.objects.get(id=alumni_id, role='alumni')
            alumni.is_approved = True
            alumni.save()
            
            return Response({'message': 'Alumni approved successfully'})
        except User.DoesNotExist:
            return Response({'error': 'Alumni not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def reject_alumni(request, alumni_id):
        """Reject an alumni"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            alumni = User.objects.get(id=alumni_id, role='alumni')
            alumni.delete()
            
            return Response({'message': 'Alumni rejected and removed'})
        except User.DoesNotExist:
            return Response({'error': 'Alumni not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def tech_heads_list(request):
        """Get list of tech heads"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        tech_heads = User.objects.filter(role='tech_head')
        
        tech_heads_data = []
        for tech_head in tech_heads:
            tech_heads_data.append({
                'id': tech_head.id,
                'username': tech_head.username,
                'first_name': tech_head.first_name,
                'last_name': tech_head.last_name,
                'email': tech_head.email,
                'date_joined': tech_head.date_joined,
                'is_approved': tech_head.is_approved,
                'is_active': tech_head.is_active
            })
        
        return Response({'tech_heads': tech_heads_data})
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def eligible_users(request):
        """Get list of users eligible to be promoted to tech head"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        # Students and teachers who are not already tech heads
        eligible = User.objects.filter(
            role__in=['student', 'teacher'],
            is_approved=True,
            is_active=True
        ).exclude(role='tech_head')
        
        eligible_data = []
        for user in eligible:
            eligible_data.append({
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role,
                'date_joined': user.date_joined
            })
        
        return Response({'eligible_users': eligible_data})
    
    @staticmethod
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def promote_to_tech_head(request):
        """Promote a user to tech head"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'User ID required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            user.role = 'tech_head'
            user.is_staff = True
            user.save()
            
            return Response({'message': f'{user.first_name} {user.last_name} promoted to Tech Head'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    @api_view(['DELETE'])
    @permission_classes([IsAuthenticated])
    def remove_tech_head(request, tech_head_id):
        """Remove tech head role"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            tech_head = User.objects.get(id=tech_head_id, role='tech_head')
            # Demote to student by default
            tech_head.role = 'student'
            tech_head.is_staff = False
            tech_head.save()
            
            return Response({'message': 'Tech head role removed'})
        except User.DoesNotExist:
            return Response({'error': 'Tech head not found'}, status=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def academic_schemes(request):
        """Get list of academic schemes"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        schemes = Scheme.objects.all()
        
        schemes_data = []
        for scheme in schemes:
            schemes_data.append({
                'id': scheme.id,
                'name': scheme.name,
                'year': scheme.year,
                'description': scheme.description,
                'is_active': scheme.is_active,
                'subjects_count': scheme.subjects.count(),
                'created_at': scheme.created_at,
                'updated_at': scheme.updated_at
            })
        
        return Response({'schemes': schemes_data})
    
    @staticmethod
    @api_view(['GET'])
    @permission_classes([IsAuthenticated])
    def subjects_list(request):
        """Get list of subjects"""
        if request.user.role != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        subjects = Subject.objects.all().select_related('scheme')
        
        subjects_data = []
        for subject in subjects:
            subjects_data.append({
                'id': subject.id,
                'name': subject.name,
                'code': subject.code,
                'scheme': subject.scheme.name,
                'scheme_id': subject.scheme.id,
                'semester': subject.semester,
                'credits': subject.credits,
                'is_active': subject.is_active,
                'created_at': subject.created_at,
                'updated_at': subject.updated_at
            })
        
        return Response({'subjects': subjects_data})
