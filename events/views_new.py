from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Event, EventRegistration
from .serializers import (
    EventSerializer, EventCreateSerializer, EventRegistrationSerializer, 
    GuestRegistrationSerializer
)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def events_list(request):
    """List all active events"""
    events = Event.objects.filter(is_active=True)
    
    # Optional filtering
    event_type = request.query_params.get('event_type')
    featured_only = request.query_params.get('featured')
    upcoming_only = request.query_params.get('upcoming')
    
    if event_type:
        events = events.filter(event_type=event_type)
    
    if featured_only and featured_only.lower() == 'true':
        events = events.filter(is_featured=True)
    
    if upcoming_only and upcoming_only.lower() == 'true':
        from django.utils import timezone
        events = events.filter(start_date__gt=timezone.now())
    
    serializer = EventSerializer(events, many=True)
    return Response({
        'events': serializer.data,
        'count': events.count()
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_event(request):
    """Create a new event (only for teachers, tech_heads, admins)"""
    if request.user.role not in ['teacher', 'tech_head', 'admin']:
        return Response(
            {'error': 'You do not have permission to create events'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = EventCreateSerializer(data=request.data)
    if serializer.is_valid():
        event = serializer.save(created_by=request.user)
        response_serializer = EventSerializer(event)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def event_detail(request, pk):
    """Get detailed view of an event"""
    event = get_object_or_404(Event, pk=pk, is_active=True)
    serializer = EventSerializer(event)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_for_event(request, event_id):
    """Register for an event (authenticated or guest)"""
    event = get_object_or_404(Event, pk=event_id, is_active=True)
    
    # Check if registration is open
    if not event.registration_open:
        return Response(
            {'error': 'Registration is not open for this event'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if request.user.is_authenticated:
        # Authenticated user registration
        if EventRegistration.objects.filter(event=event, user=request.user).exists():
            return Response(
                {'error': 'You are already registered for this event'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        registration = EventRegistration.objects.create(
            event=event,
            user=request.user,
            is_confirmed=True
        )
        
        serializer = EventRegistrationSerializer(registration)
        return Response({
            'message': 'Successfully registered for the event',
            'registration': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    else:
        # Guest registration
        serializer = GuestRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Check for duplicate guest registration by email
            if EventRegistration.objects.filter(
                event=event, 
                guest_email=serializer.validated_data['guest_email']
            ).exists():
                return Response(
                    {'error': 'This email is already registered for this event'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            registration = EventRegistration.objects.create(
                event=event,
                is_confirmed=True,
                **serializer.validated_data
            )
            
            response_serializer = EventRegistrationSerializer(registration)
            return Response({
                'message': 'Successfully registered for the event',
                'registration': response_serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def event_registrations(request, event_id):
    """Get all registrations for an event (only for event creators, tech_heads, admins)"""
    event = get_object_or_404(Event, pk=event_id, is_active=True)
    
    # Check permissions
    if not (request.user.role in ['tech_head', 'admin'] or event.created_by == request.user):
        return Response(
            {'error': 'You do not have permission to view registrations'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    registrations = EventRegistration.objects.filter(event=event, is_confirmed=True)
    serializer = EventRegistrationSerializer(registrations, many=True)
    
    return Response({
        'registrations': serializer.data,
        'total_registrations': registrations.count(),
        'event': EventSerializer(event).data
    })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_registrations(request):
    """Get user's event registrations"""
    registrations = EventRegistration.objects.filter(
        user=request.user, 
        is_confirmed=True
    ).select_related('event')
    
    serializer = EventRegistrationSerializer(registrations, many=True)
    return Response({
        'registrations': serializer.data,
        'count': registrations.count()
    })
