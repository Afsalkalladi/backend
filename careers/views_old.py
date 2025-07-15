from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from .models import JobOpportunity
from .serializers import JobOpportunitySerializer, JobOpportunityCreateSerializer

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def job_opportunities_list(request):
    """
    List all active job opportunities with optional filtering
    """
    opportunities = JobOpportunity.objects.filter(is_active=True)
    
    # Optional filtering
    job_type = request.query_params.get('job_type')
    experience_level = request.query_params.get('experience_level')
    location = request.query_params.get('location')
    search = request.query_params.get('search')
    
    if job_type:
        opportunities = opportunities.filter(job_type=job_type)
    
    if experience_level:
        opportunities = opportunities.filter(experience_level=experience_level)
    
    if location:
        opportunities = opportunities.filter(location__icontains=location)
    
    if search:
        opportunities = opportunities.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(description__icontains=search) |
            Q(skills__icontains=search)
        )
    
    serializer = JobOpportunitySerializer(opportunities, many=True)
    
    # Also return available filter options
    job_types = JobOpportunity.JOB_TYPES
    experience_levels = JobOpportunity.EXPERIENCE_LEVELS
    
    return Response({
        'opportunities': serializer.data,
        'job_types': dict(job_types),
        'experience_levels': dict(experience_levels),
        'count': opportunities.count()
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_job_opportunity(request):
    """
    Create a new job opportunity (only for teachers, alumni, tech_heads, admins)
    """
    if request.user.role not in ['teacher', 'alumni', 'tech_head', 'admin']:
        return Response(
            {'error': 'You do not have permission to post job opportunities'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = JobOpportunityCreateSerializer(data=request.data)
    if serializer.is_valid():
        job_opportunity = serializer.save(posted_by=request.user)
        response_serializer = JobOpportunitySerializer(job_opportunity)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def job_opportunity_detail(request, pk):
    """
    Get detailed view of a job opportunity
    """
    try:
        opportunity = JobOpportunity.objects.get(pk=pk, is_active=True)
        serializer = JobOpportunitySerializer(opportunity)
        return Response(serializer.data)
    except JobOpportunity.DoesNotExist:
        return Response(
            {'error': 'Job opportunity not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
