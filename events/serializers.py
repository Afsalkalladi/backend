from rest_framework import serializers
from .models import Event
from accounts.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    """Event serializer"""
    
    created_by = UserSerializer(read_only=True)
    is_upcoming = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'time', 'venue',
            'created_by', 'is_active', 'is_upcoming', 'is_past',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class EventCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating events"""
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue']
    
    def validate_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past")
        return value
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class EventUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating events"""
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'time', 'venue', 'is_active']
    
    def validate_date(self, value):
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past")
        return value


class EventListSerializer(serializers.ModelSerializer):
    """Simplified event serializer for lists"""
    
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'date', 'time', 'venue', 'created_by_name', 'is_active'
        ]


class UpcomingEventSerializer(serializers.ModelSerializer):
    """Serializer for upcoming events ticker"""
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'date', 'time', 'venue']
