from rest_framework import serializers
from .models import Subject, Note
from accounts.serializers import UserSerializer


class SubjectSerializer(serializers.ModelSerializer):
    """Subject serializer"""
    
    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'code', 'scheme', 'semester', 'credits', 
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NoteSerializer(serializers.ModelSerializer):
    """Note serializer"""
    
    uploaded_by = UserSerializer(read_only=True)
    approved_by = UserSerializer(read_only=True)
    subject_details = SubjectSerializer(source='subject', read_only=True)
    
    class Meta:
        model = Note
        fields = [
            'id', 'title', 'description', 'subject', 'subject_details',
            'uploaded_by', 'file', 'is_approved', 'approved_by', 
            'approved_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'uploaded_by', 'is_approved', 'approved_by', 
            'approved_at', 'created_at', 'updated_at'
        ]


class NoteUploadSerializer(serializers.ModelSerializer):
    """Serializer for uploading notes"""
    
    class Meta:
        model = Note
        fields = ['title', 'description', 'subject', 'file']
    
    def validate_subject(self, value):
        if not value.is_active:
            raise serializers.ValidationError("This subject is not active")
        return value
    
    def create(self, validated_data):
        validated_data['uploaded_by'] = self.context['request'].user
        return super().create(validated_data)


class NoteApprovalSerializer(serializers.Serializer):
    """Serializer for note approval"""
    
    note_id = serializers.IntegerField()
    
    def validate_note_id(self, value):
        try:
            note = Note.objects.get(pk=value)
            if note.is_approved:
                raise serializers.ValidationError("Note is already approved")
            return value
        except Note.DoesNotExist:
            raise serializers.ValidationError("Note not found")


class SubjectsBySchemeSerializer(serializers.Serializer):
    """Serializer for getting subjects by scheme and semester"""
    
    scheme = serializers.IntegerField()
    semester = serializers.IntegerField(min_value=1, max_value=8)
    
    def validate(self, attrs):
        scheme = attrs['scheme']
        semester = attrs['semester']
        
        if not Subject.objects.filter(scheme=scheme, semester=semester, is_active=True).exists():
            raise serializers.ValidationError(
                f"No active subjects found for scheme {scheme}, semester {semester}"
            )
        
        return attrs
