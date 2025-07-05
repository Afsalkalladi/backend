from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.db import transaction
from accounts.permissions import IsAdminOrTechnicalHead, IsTeacherOrAdminOrTechnicalHead
from .models import Student, Reviewer
from .serializers import (
    StudentSerializer, StudentListSerializer, StudentUpdateSerializer,
    BulkPromotionSerializer, ReviewerSerializer, ReviewerAssignmentSerializer
)


@api_view(['GET'])
@permission_classes([IsTeacherOrAdminOrTechnicalHead])
def student_list(request):
    """List students grouped by scheme and year"""
    scheme = request.GET.get('scheme')
    year_of_joining = request.GET.get('year_of_joining')
    semester = request.GET.get('semester')
    
    queryset = Student.objects.all()
    
    if scheme:
        queryset = queryset.filter(scheme=scheme)
    if year_of_joining:
        queryset = queryset.filter(year_of_joining=year_of_joining)
    if semester:
        queryset = queryset.filter(ongoing_semester=semester)
    
    students = queryset.order_by('scheme', 'year_of_joining', 'full_name')
    
    # Group by scheme and year
    grouped_data = {}
    for student in students:
        key = f"S{student.scheme}_Y{student.year_of_joining}"
        if key not in grouped_data:
            grouped_data[key] = {
                'scheme': student.scheme,
                'year_of_joining': student.year_of_joining,
                'students': []
            }
        grouped_data[key]['students'].append(StudentListSerializer(student).data)
    
    return Response({
        'groups': list(grouped_data.values()),
        'total_students': len(students)
    })


@api_view(['GET'])
@permission_classes([IsTeacherOrAdminOrTechnicalHead])
def student_detail(request, pk):
    """Get detailed student information"""
    try:
        student = Student.objects.select_related('user').get(pk=pk)
        return Response(StudentSerializer(student).data)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminOrTechnicalHead])
def update_student(request, pk):
    """Update student academic information (semester, year)"""
    try:
        student = Student.objects.get(pk=pk)
        serializer = StudentUpdateSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Student updated successfully',
                'student': StudentSerializer(student).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAdminOrTechnicalHead])
def bulk_promote_students(request):
    """Promote students in bulk to next semester"""
    serializer = BulkPromotionSerializer(data=request.data)
    if serializer.is_valid():
        scheme = serializer.validated_data['scheme']
        current_semester = serializer.validated_data['current_semester']
        
        if current_semester >= 8:
            return Response({
                'error': 'Cannot promote students beyond semester 8'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            students = Student.objects.filter(
                scheme=scheme,
                ongoing_semester=current_semester
            )
            
            promoted_count = 0
            for student in students:
                student.ongoing_semester += 1
                student.save()  # This will auto-update year_of_study
                promoted_count += 1
        
        return Response({
            'message': f'Successfully promoted {promoted_count} students from semester {current_semester} to {current_semester + 1}',
            'promoted_count': promoted_count
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminOrTechnicalHead])
def reviewers_list(request):
    """List all active reviewers"""
    reviewers = Reviewer.objects.filter(is_active=True).select_related('student__user')
    return Response({
        'reviewers': ReviewerSerializer(reviewers, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAdminOrTechnicalHead])
def assign_reviewer(request):
    """Assign a student as reviewer for specific scheme and year"""
    serializer = ReviewerAssignmentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        reviewer = serializer.save()
        return Response({
            'message': 'Reviewer assigned successfully',
            'reviewer': ReviewerSerializer(reviewer).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminOrTechnicalHead])
def remove_reviewer(request, pk):
    """Remove/deactivate a reviewer"""
    try:
        reviewer = Reviewer.objects.get(pk=pk, is_active=True)
        reviewer.is_active = False
        reviewer.save()
        return Response({
            'message': 'Reviewer removed successfully'
        })
    except Reviewer.DoesNotExist:
        return Response({'error': 'Active reviewer not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_student_profile(request):
    """Get current user's student profile"""
    if request.user.role != 'student':
        return Response({'error': 'Only students can access this endpoint'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        student = Student.objects.get(user=request.user)
        return Response(StudentSerializer(student).data)
    except Student.DoesNotExist:
        return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
