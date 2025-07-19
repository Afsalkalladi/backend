from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from .models import AcademicCategory, AcademicResource, Scheme, Subject

@api_view(['GET'])
@permission_classes([])  # Remove authentication requirement
def academic_categories_list(request):
    """List all academic categories"""
    categories = AcademicCategory.objects.all().values(
        'id', 'name', 'category_type', 'description', 'icon', 'is_active'
    )
    return Response(list(categories))

@api_view(['GET'])
@permission_classes([])  # Remove authentication requirement
def category_detail(request, category_type):
    """Get category details and its resources"""
    try:
        # Get the first category of this type (in case there are duplicates)
        category = AcademicCategory.objects.filter(category_type=category_type).first()
        if not category:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
            
        resources = AcademicResource.objects.filter(category__category_type=category_type, is_approved=True)
        
        # Filter by query parameters
        scheme_id = request.GET.get('scheme')
        subject_id = request.GET.get('subject')
        semester = request.GET.get('semester')
        
        if scheme_id:
            resources = resources.filter(scheme_id=scheme_id)
        if subject_id:
            resources = resources.filter(subject_id=subject_id)
        if semester:
            resources = resources.filter(semester=semester)
            
        category_data = {
            'id': category.id,
            'name': category.name,
            'category_type': category.category_type,
            'description': category.description,
            'icon': category.icon,
            'is_active': category.is_active
        }
        
        resources_data = list(resources.values(
            'id', 'title', 'description', 'file', 'file_size',
            'module_number', 'exam_type', 'exam_year', 'author',
            'download_count', 'created_at', 'updated_at'
        ))
        
        return Response({
            'category': category_data,
            'resources': resources_data
        })
    except AcademicCategory.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([])  # Remove authentication requirement
def academic_resources_list(request):
    """List academic resources with filtering"""
    resources = AcademicResource.objects.filter(is_approved=True).select_related(
        'category', 'subject', 'uploaded_by'
    )
    
    # Filter by category type
    category_type = request.GET.get('category_type')
    if category_type:
        resources = resources.filter(category__category_type=category_type)
    
    # Filter by other parameters
    scheme_id = request.GET.get('scheme')
    subject_id = request.GET.get('subject')
    semester = request.GET.get('semester')
    search = request.GET.get('search')
    
    if scheme_id:
        resources = resources.filter(scheme_id=scheme_id)
    if subject_id:
        resources = resources.filter(subject_id=subject_id)
    if semester:
        resources = resources.filter(semester=semester)
    if search:
        resources = resources.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search)
        )
    
    resources_data = []
    for resource in resources:
        resources_data.append({
            'id': resource.id,
            'title': resource.title,
            'description': resource.description,
            'file': resource.file.url if resource.file else '',
            'file_size': resource.file_size,
            'module_number': resource.module_number,
            'exam_type': resource.exam_type,
            'exam_year': resource.exam_year,
            'author': resource.author,
            'download_count': resource.download_count,
            'created_at': resource.created_at,
            'updated_at': resource.updated_at,
            'category': resource.category.category_type,
            'category_name': resource.category.name,
            'subject_name': resource.subject.name,
            'subject_code': resource.subject.code,
            'is_featured': resource.is_featured,
            'uploaded_by_name': f"{resource.uploaded_by.first_name} {resource.uploaded_by.last_name}",
        })
    return Response(resources_data)

@api_view(['GET'])
def academic_resource_detail(request, pk):
    """Get single academic resource"""
    try:
        resource = AcademicResource.objects.get(pk=pk, is_approved=True)
        resource_data = {
            'id': resource.id,
            'title': resource.title,
            'description': resource.description,
            'file': resource.file.url if resource.file else None,
            'file_size': resource.file_size,
            'module_number': resource.module_number,
            'exam_type': resource.exam_type,
            'exam_year': resource.exam_year,
            'author': resource.author,
            'created_at': resource.created_at,
            'updated_at': resource.updated_at
        }
        return Response(resource_data)
    except AcademicResource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_academic_resource(request):
    """Upload new academic resource"""
    # Simple validation and creation
    required_fields = ['title', 'category', 'file']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # File validation
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return Response({'error': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Check file extension
    if not uploaded_file.name.lower().endswith('.pdf'):
        return Response({
            'error': 'Only PDF files are allowed. Please upload a PDF document.',
            'help_text': 'Upload only PDF files. Maximum file size: 15MB. Only PDF format is supported for academic resources.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check file size (15MB limit)
    if uploaded_file.size > 15 * 1024 * 1024:
        return Response({
            'error': 'File size must be less than 15MB. Please compress the file or use a smaller document.',
            'help_text': 'Upload only PDF files. Maximum file size: 15MB. Only PDF format is supported for academic resources.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        category = AcademicCategory.objects.get(id=request.data['category'])
        resource = AcademicResource.objects.create(
            title=request.data['title'],
            description=request.data.get('description', ''),
            category=category,
            file=uploaded_file,
            uploaded_by=request.user,
            module_number=request.data.get('module_number', 1),
            exam_type=request.data.get('exam_type', ''),
            exam_year=request.data.get('exam_year'),
            author=request.data.get('author', '')
        )
        return Response({'id': resource.id, 'message': 'Resource uploaded successfully'}, 
                       status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def schemes_list(request):
    """List all academic schemes"""
    schemes = Scheme.objects.all().values('id', 'year', 'name', 'description', 'is_active')
    return Response(list(schemes))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_scheme(request):
    """Create new academic scheme"""
    try:
        scheme = Scheme.objects.create(
            year=request.data['year'],
            name=request.data['name'],
            description=request.data.get('description', ''),
            is_active=request.data.get('is_active', True)
        )
        return Response({'id': scheme.id, 'message': 'Scheme created successfully'}, 
                       status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def subjects_by_scheme_semester(request):
    """Get subjects filtered by scheme and semester"""
    scheme_id = request.GET.get('scheme')
    semester = request.GET.get('semester')
    
    subjects = Subject.objects.all()
    
    if scheme_id:
        subjects = subjects.filter(scheme_id=scheme_id)
    if semester:
        subjects = subjects.filter(semester=semester)
        
    subjects_data = list(subjects.values('id', 'name', 'code', 'semester', 'credits'))
    return Response(subjects_data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_subject(request):
    """Create new subject"""
    try:
        subject = Subject.objects.create(
            name=request.data['name'],
            code=request.data['code'],
            semester=request.data['semester'],
            credits=request.data.get('credits', 3),
            scheme_id=request.data.get('scheme'),
            description=request.data.get('description', '')
        )
        return Response({'id': subject.id, 'message': 'Subject created successfully'}, 
                       status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([])  # Remove authentication requirement
def download_academic_resource(request, pk):
    """Download academic resource file"""
    try:
        resource = AcademicResource.objects.get(pk=pk, is_approved=True)
        
        if not resource.file:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Increment download count
        resource.download_count += 1
        resource.save()
        
        # Get the file path
        file_path = resource.file.path
        
        if not os.path.exists(file_path):
            return Response({'error': 'File not found on disk'}, status=status.HTTP_404_NOT_FOUND)
        
        # Open and serve the file
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
            
    except AcademicResource.DoesNotExist:
        return Response({'error': 'Resource not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
