from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from accounts.permissions import (
    IsAdminOrTechnicalHead, IsStudentOrAdminOrTechnicalHead, CanApproveNotes, IsOwnerOrReadOnly
)
from .models import Subject, Note
from .serializers import (
    SubjectSerializer, NoteSerializer, NoteUploadSerializer, 
    NoteApprovalSerializer, SubjectsBySchemeSerializer
)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def subjects_by_scheme_semester(request):
    """Get subjects by scheme and semester"""
    scheme = request.GET.get('scheme')
    semester = request.GET.get('semester')
    
    if not scheme or not semester:
        return Response({
            'error': 'Both scheme and semester parameters are required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        scheme = int(scheme)
        semester = int(semester)
    except ValueError:
        return Response({
            'error': 'Scheme and semester must be integers'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    subjects = Subject.objects.filter(
        scheme=scheme, 
        semester=semester, 
        is_active=True
    ).order_by('name')
    
    return Response({
        'scheme': scheme,
        'semester': semester,
        'subjects': SubjectSerializer(subjects, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAdminOrTechnicalHead])
def create_subject(request):
    """Create a new subject"""
    serializer = SubjectSerializer(data=request.data)
    if serializer.is_valid():
        subject = serializer.save()
        return Response({
            'message': 'Subject created successfully',
            'subject': SubjectSerializer(subject).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def notes_list(request):
    """List notes with filtering options"""
    scheme = request.GET.get('scheme')
    semester = request.GET.get('semester')
    subject_id = request.GET.get('subject')
    approved_only = request.GET.get('approved_only', 'true').lower() == 'true'
    
    queryset = Note.objects.all()
    
    if approved_only:
        queryset = queryset.filter(is_approved=True)
    
    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)
    elif scheme and semester:
        queryset = queryset.filter(subject__scheme=scheme, subject__semester=semester)
    
    # Order by approval status and creation date
    queryset = queryset.order_by('-is_approved', '-created_at')
    
    notes = queryset.select_related('subject', 'uploaded_by', 'approved_by')
    
    return Response({
        'notes': NoteSerializer(notes, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsStudentOrAdminOrTechnicalHead])
def upload_note(request):
    """Upload a new note"""
    serializer = NoteUploadSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        note = serializer.save()
        return Response({
            'message': 'Note uploaded successfully',
            'note': NoteSerializer(note).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([CanApproveNotes])
def approve_note(request):
    """Approve a note"""
    serializer = NoteApprovalSerializer(data=request.data)
    if serializer.is_valid():
        note_id = serializer.validated_data['note_id']
        
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if user can approve this specific note
        if not note.can_be_approved_by(request.user):
            return Response({
                'error': 'You are not authorized to approve this note'
            }, status=status.HTTP_403_FORBIDDEN)
        
        note.is_approved = True
        note.approved_by = request.user
        note.approved_at = timezone.now()
        note.save()
        
        return Response({
            'message': 'Note approved successfully',
            'note': NoteSerializer(note).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_notes(request):
    """Get current user's uploaded notes"""
    notes = Note.objects.filter(uploaded_by=request.user).order_by('-created_at')
    return Response({
        'notes': NoteSerializer(notes, many=True).data
    })


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_note(request, pk):
    """Delete a note (only by uploader or admin)"""
    try:
        note = Note.objects.get(pk=pk)
        
        # Check permissions
        if note.uploaded_by != request.user and request.user.role != 'admin':
            return Response({
                'error': 'You can only delete your own notes'
            }, status=status.HTTP_403_FORBIDDEN)
        
        note.delete()
        return Response({'message': 'Note deleted successfully'})
        
    except Note.DoesNotExist:
        return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([CanApproveNotes])
def pending_notes(request):
    """Get notes pending approval that current user can approve"""
    notes = Note.objects.filter(is_approved=False).order_by('-created_at')
    
    # Filter notes that current user can approve
    approvable_notes = []
    for note in notes:
        if note.can_be_approved_by(request.user):
            approvable_notes.append(note)
    
    return Response({
        'pending_notes': NoteSerializer(approvable_notes, many=True).data,
        'count': len(approvable_notes)
    })
