from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from accounts.permissions import IsAdminOrTechnicalHead
from .models import Event
from .serializers import (
    EventSerializer, EventCreateSerializer, EventUpdateSerializer, 
    EventListSerializer, UpcomingEventSerializer
)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def events_list(request):
    """List all events with filtering"""
    show_past = request.GET.get('show_past', 'false').lower() == 'true'
    
    queryset = Event.objects.filter(is_active=True)
    
    if not show_past:
        # Filter to show only upcoming events
        today = timezone.now().date()
        queryset = queryset.filter(date__gte=today)
    
    events = queryset.order_by('date', 'time').select_related('created_by')
    
    return Response({
        'events': EventListSerializer(events, many=True).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def event_detail(request, pk):
    """Get detailed event information"""
    try:
        event = Event.objects.select_related('created_by').get(pk=pk)
        return Response(EventSerializer(event).data)
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAdminOrTechnicalHead])
def create_event(request):
    """Create a new event"""
    serializer = EventCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        event = serializer.save()
        return Response({
            'message': 'Event created successfully',
            'event': EventSerializer(event).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminOrTechnicalHead])
def update_event(request, pk):
    """Update an event"""
    try:
        event = Event.objects.get(pk=pk)
        serializer = EventUpdateSerializer(event, data=request.data, partial=True)
        if serializer.is_valid():
            event = serializer.save()
            return Response({
                'message': 'Event updated successfully',
                'event': EventSerializer(event).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAdminOrTechnicalHead])
def delete_event(request, pk):
    """Delete an event (soft delete by setting is_active=False)"""
    try:
        event = Event.objects.get(pk=pk)
        event.is_active = False
        event.save()
        return Response({'message': 'Event deleted successfully'})
        
    except Event.DoesNotExist:
        return Response({'error': 'Event not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def upcoming_events_ticker(request):
    """Get upcoming events for homepage ticker"""
    today = timezone.now().date()
    
    # Get next 10 upcoming events
    upcoming_events = Event.objects.filter(
        date__gte=today,
        is_active=True
    ).order_by('date', 'time')[:10]
    
    return Response({
        'upcoming_events': UpcomingEventSerializer(upcoming_events, many=True).data
    })


@api_view(['GET'])
@permission_classes([IsAdminOrTechnicalHead])
def my_events(request):
    """Get events created by current user"""
    events = Event.objects.filter(created_by=request.user).order_by('-created_at')
    return Response({
        'events': EventSerializer(events, many=True).data
    })
