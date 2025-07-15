from rest_framework import serializers
from .models import GalleryCategory, GalleryImage, GalleryAlbum, AlbumImage


class GalleryCategorySerializer(serializers.ModelSerializer):
    image_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'description', 'slug', 'image_count', 'is_active']
    
    def get_image_count(self, obj):
        return obj.images.filter(is_public=True).count()


class GalleryImageSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    tag_list = serializers.ReadOnlyField()
    file_size_mb = serializers.ReadOnlyField()
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'description', 'image', 'thumbnail',
            'category', 'category_name', 'tags', 'tag_list',
            'event_name', 'event_date', 'location',
            'photographer', 'camera_info',
            'is_featured', 'is_public', 'display_order',
            'uploaded_by_name', 'file_size_mb',
            'image_width', 'image_height',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['uploaded_by', 'file_size', 'image_width', 'image_height']


class GalleryImageListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing images"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'image', 'thumbnail',
            'category_name', 'event_name', 'event_date',
            'is_featured', 'created_at'
        ]


class AlbumImageSerializer(serializers.ModelSerializer):
    image = GalleryImageListSerializer(read_only=True)
    
    class Meta:
        model = AlbumImage
        fields = ['image', 'order']


class GalleryAlbumSerializer(serializers.ModelSerializer):
    images = AlbumImageSerializer(many=True, read_only=True)
    cover_image = GalleryImageListSerializer(read_only=True)
    image_count = serializers.ReadOnlyField()
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = GalleryAlbum
        fields = [
            'id', 'name', 'description', 'slug', 'cover_image',
            'event_date', 'location',
            'is_public', 'is_featured', 'display_order',
            'image_count', 'created_by_name',
            'created_at', 'updated_at', 'images'
        ]
        read_only_fields = ['created_by']


class GalleryAlbumListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing albums"""
    cover_image = GalleryImageListSerializer(read_only=True)
    image_count = serializers.ReadOnlyField()
    
    class Meta:
        model = GalleryAlbum
        fields = [
            'id', 'name', 'description', 'slug', 'cover_image',
            'event_date', 'location', 'image_count',
            'is_featured', 'created_at'
        ]
