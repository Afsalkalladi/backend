from rest_framework import serializers
from .models import Student, Reviewer
from accounts.serializers import UserSerializer


class StudentSerializer(serializers.ModelSerializer):
    """Student serializer"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'user', 'full_name', 'scheme', 'year_of_joining', 
            'expected_year_of_passout', 'ongoing_semester', 'year_of_study',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class StudentListSerializer(serializers.ModelSerializer):
    """Simplified student serializer for lists"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    mobile_number = serializers.CharField(source='user.mobile_number', read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'username', 'email', 'full_name', 'mobile_number', 'scheme', 
            'year_of_joining', 'ongoing_semester', 'year_of_study'
        ]


class StudentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating student academic information"""
    
    class Meta:
        model = Student
        fields = ['ongoing_semester', 'year_of_study']
    
    def validate_ongoing_semester(self, value):
        if value not in range(1, 9):
            raise serializers.ValidationError("Semester must be between 1 and 8")
        return value
    
    def validate_year_of_study(self, value):
        if value not in range(1, 5):
            raise serializers.ValidationError("Year of study must be between 1 and 4")
        return value


class BulkPromotionSerializer(serializers.Serializer):
    """Serializer for bulk semester promotion"""
    
    scheme = serializers.IntegerField()
    current_semester = serializers.IntegerField(min_value=1, max_value=8)
    
    def validate(self, attrs):
        scheme = attrs['scheme']
        current_semester = attrs['current_semester']
        
        # Check if students exist for this scheme and semester
        if not Student.objects.filter(scheme=scheme, ongoing_semester=current_semester).exists():
            raise serializers.ValidationError(
                f"No students found for scheme {scheme} in semester {current_semester}"
            )
        
        return attrs


class ReviewerSerializer(serializers.ModelSerializer):
    """Reviewer serializer"""
    
    student = StudentListSerializer(read_only=True)
    assigned_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Reviewer
        fields = [
            'id', 'student', 'scheme', 'year_of_joining', 
            'assigned_by', 'assigned_at', 'is_active'
        ]
        read_only_fields = ['id', 'assigned_at']


class ReviewerAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for assigning reviewers"""
    
    student_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Reviewer
        fields = ['student_id', 'scheme', 'year_of_joining']
    
    def validate_student_id(self, value):
        try:
            student = Student.objects.get(pk=value)
            if student.user.role != 'student':
                raise serializers.ValidationError("Selected user is not a student")
            return value
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student not found")
    
    def validate(self, attrs):
        student_id = attrs['student_id']
        scheme = attrs['scheme']
        year_of_joining = attrs['year_of_joining']
        
        # Verify the student belongs to the specified scheme and year
        try:
            student = Student.objects.get(
                pk=student_id,
                scheme=scheme,
                year_of_joining=year_of_joining
            )
        except Student.DoesNotExist:
            raise serializers.ValidationError(
                "Student doesn't belong to the specified scheme and year"
            )
        
        return attrs
    
    def create(self, validated_data):
        student_id = validated_data.pop('student_id')
        student = Student.objects.get(pk=student_id)
        
        reviewer = Reviewer.objects.create(
            student=student,
            assigned_by=self.context['request'].user,
            **validated_data
        )
        return reviewer
