from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from students.models import Student

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    # Alumni specific fields
    year_of_passout = serializers.IntegerField(required=False, allow_null=True)
    current_workplace = serializers.CharField(required=False, allow_blank=True, max_length=200)
    job_title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    linkedin_url = serializers.URLField(required=False, allow_blank=True)
    
    # Student specific fields
    full_name = serializers.CharField(required=False, max_length=100)
    scheme = serializers.IntegerField(required=False)
    year_of_joining = serializers.IntegerField(required=False)
    expected_year_of_passout = serializers.IntegerField(required=False)
    ongoing_semester = serializers.IntegerField(required=False)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm', 'role', 'mobile_number',
            'first_name', 'last_name',
            # Alumni fields
            'year_of_passout', 'current_workplace', 'job_title', 'linkedin_url',
            # Student fields
            'full_name', 'scheme', 'year_of_joining', 'expected_year_of_passout', 'ongoing_semester'
        ]
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        role = attrs.get('role')
        
        # Validate alumni fields
        if role == 'alumni':
            if not attrs.get('year_of_passout'):
                raise serializers.ValidationError("Year of passout is required for alumni")
        
        # Validate student fields
        if role == 'student':
            required_fields = ['full_name', 'scheme', 'year_of_joining', 'expected_year_of_passout', 'ongoing_semester']
            for field in required_fields:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"{field.replace('_', ' ').title()} is required for students")
            
            if attrs.get('ongoing_semester') not in range(1, 9):
                raise serializers.ValidationError("Ongoing semester must be between 1 and 8")
        
        return attrs
    
    def create(self, validated_data):
        # Remove password_confirm and student/alumni specific fields
        validated_data.pop('password_confirm')
        student_data = {}
        if validated_data.get('role') == 'student':
            student_fields = ['full_name', 'scheme', 'year_of_joining', 'expected_year_of_passout', 'ongoing_semester']
            for field in student_fields:
                if field in validated_data:
                    student_data[field] = validated_data.pop(field)
        
        # Create user
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create student profile if role is student
        if user.role == 'student' and student_data:
            Student.objects.create(user=user, **student_data)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """User serializer for profile information"""
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role', 
            'mobile_number', 'year_of_passout', 'current_workplace', 
            'job_title', 'linkedin_url', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class LoginSerializer(serializers.Serializer):
    """Login serializer"""
    
    username_or_email = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')
        
        if username_or_email and password:
            # Try to authenticate with username first, then email
            user = authenticate(username=username_or_email, password=password)
            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user and user.is_active:
                attrs['user'] = user
                return attrs
            else:
                raise serializers.ValidationError('Invalid credentials or inactive account')
        else:
            raise serializers.ValidationError('Must include username/email and password')
