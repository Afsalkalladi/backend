from rest_framework import serializers
from .models import Project, TeamMember
from accounts.serializers import UserSerializer


class TeamMemberSerializer(serializers.ModelSerializer):
    """Team member serializer"""
    
    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'linkedin_url', 'role']
        read_only_fields = ['id']


class ProjectSerializer(serializers.ModelSerializer):
    """Project serializer"""
    
    created_by = UserSerializer(read_only=True)
    team_members = TeamMemberSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'category', 'github_url', 
            'demo_url', 'created_by', 'team_members', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class ProjectCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating projects"""
    
    team_members = TeamMemberSerializer(many=True, required=False)
    
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'category', 'github_url', 
            'demo_url', 'team_members'
        ]
    
    def create(self, validated_data):
        team_members_data = validated_data.pop('team_members', [])
        
        # Create project
        project = Project.objects.create(
            created_by=self.context['request'].user,
            **validated_data
        )
        
        # Create team members
        for member_data in team_members_data:
            TeamMember.objects.create(project=project, **member_data)
        
        return project


class ProjectUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating projects"""
    
    team_members = TeamMemberSerializer(many=True, required=False)
    
    class Meta:
        model = Project
        fields = [
            'title', 'description', 'category', 'github_url', 
            'demo_url', 'team_members'
        ]
    
    def update(self, instance, validated_data):
        team_members_data = validated_data.pop('team_members', None)
        
        # Update project fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update team members if provided
        if team_members_data is not None:
            # Remove existing team members
            instance.team_members.all().delete()
            
            # Create new team members
            for member_data in team_members_data:
                TeamMember.objects.create(project=instance, **member_data)
        
        return instance


class ProjectListSerializer(serializers.ModelSerializer):
    """Simplified project serializer for lists"""
    
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    team_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'category', 'github_url', 
            'demo_url', 'created_by_name', 'team_count', 'created_at'
        ]
    
    def get_team_count(self, obj):
        return obj.team_members.count()
