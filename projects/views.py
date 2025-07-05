from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.permissions import IsOwnerOrReadOnly
from .models import Project
from .serializers import (
    ProjectSerializer, ProjectCreateSerializer, ProjectUpdateSerializer, ProjectListSerializer
)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def projects_list(request):
    """List all projects with filtering"""
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    queryset = Project.objects.all()
    
    if category:
        queryset = queryset.filter(category=category)
    
    if search:
        queryset = queryset.filter(
            title__icontains=search
        )
    
    projects = queryset.order_by('-created_at').select_related('created_by')
    
    return Response({
        'projects': ProjectListSerializer(projects, many=True).data,
        'categories': dict(Project.CATEGORY_CHOICES)
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def project_detail(request, pk):
    """Get detailed project information"""
    try:
        project = Project.objects.select_related('created_by').prefetch_related('team_members').get(pk=pk)
        return Response(ProjectSerializer(project).data)
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_project(request):
    """Create a new project"""
    serializer = ProjectCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        project = serializer.save()
        return Response({
            'message': 'Project created successfully',
            'project': ProjectSerializer(project).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
def update_project(request, pk):
    """Update a project (only by creator)"""
    try:
        project = Project.objects.get(pk=pk)
        
        # Check if user is the creator
        if project.created_by != request.user:
            return Response({
                'error': 'You can only edit your own projects'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProjectUpdateSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            project = serializer.save()
            return Response({
                'message': 'Project updated successfully',
                'project': ProjectSerializer(project).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_project(request, pk):
    """Delete a project (only by creator or admin)"""
    try:
        project = Project.objects.get(pk=pk)
        
        # Check if user is the creator or admin
        if project.created_by != request.user and request.user.role != 'admin':
            return Response({
                'error': 'You can only delete your own projects'
            }, status=status.HTTP_403_FORBIDDEN)
        
        project.delete()
        return Response({'message': 'Project deleted successfully'})
        
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_projects(request):
    """Get current user's projects"""
    projects = Project.objects.filter(created_by=request.user).order_by('-created_at')
    return Response({
        'projects': ProjectSerializer(projects, many=True).data
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_projects(request):
    """Get featured projects for homepage"""
    # Get latest 6 projects for homepage display
    projects = Project.objects.order_by('-created_at')[:6].select_related('created_by')
    return Response({
        'featured_projects': ProjectListSerializer(projects, many=True).data
    })
