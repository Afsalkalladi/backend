from rest_framework import serializers
from .models import Alumni


class AlumniSerializer(serializers.ModelSerializer):
    """
    Alumni serializer
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Alumni
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'mobile_number',
            'student_id', 'branch', 'year_of_admission', 'year_of_passout', 'cgpa',
            'current_workplace', 'job_title', 'current_location', 'linkedin_url',
            'achievements', 'willing_to_mentor', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def create(self, validated_data):
        """Override create to set created_by"""
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class AlumniListSerializer(serializers.ModelSerializer):
    """
    Alumni list serializer for simplified display
    """
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Alumni
        fields = [
            'id', 'full_name', 'year_of_passout', 'current_workplace', 
            'job_title', 'current_location', 'willing_to_mentor'
        ]
