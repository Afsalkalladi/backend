from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import GalleryCategory, GalleryImage, GalleryAlbum
from .serializers import (
    GalleryCategorySerializer, GalleryImageSerializer, GalleryImageListSerializer,
    GalleryAlbumSerializer, GalleryAlbumListSerializer
)


class GalleryCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for gallery categories
    """
    queryset = GalleryCategory.objects.filter(is_active=True)
    serializer_class = GalleryCategorySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering = ['name']


class GalleryImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for gallery images
    """
    queryset = GalleryImage.objects.filter(is_public=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'event_date']
    search_fields = ['title', 'description', 'event_name', 'tags', 'photographer']
    ordering = ['-is_featured', '-display_order', '-created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GalleryImageListSerializer
        return GalleryImageSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by category slug if provided
        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tags if provided
        tags = self.request.query_params.get('tags')
        if tags:
            tag_list = [tag.strip() for tag in tags.split(',')]
            tag_query = Q()
            for tag in tag_list:
                tag_query |= Q(tags__icontains=tag)
            queryset = queryset.filter(tag_query)
        
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
    def get_permissions(self):
        """
        Allow public access for viewing, require authentication for create/update/delete
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured images"""
        featured_images = self.get_queryset().filter(is_featured=True)[:12]
        serializer = self.get_serializer(featured_images, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent images"""
        recent_images = self.get_queryset().order_by('-created_at')[:20]
        serializer = self.get_serializer(recent_images, many=True)
        return Response(serializer.data)


class GalleryAlbumViewSet(viewsets.ModelViewSet):
    """
    ViewSet for gallery albums
    """
    queryset = GalleryAlbum.objects.filter(is_public=True)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'location']
    ordering = ['-is_featured', '-display_order', '-created_at']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return GalleryAlbumListSerializer
        return GalleryAlbumSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_permissions(self):
        """
        Allow public access for viewing, require authentication for create/update/delete
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        else:
            return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured albums"""
        featured_albums = self.get_queryset().filter(is_featured=True)[:8]
        serializer = self.get_serializer(featured_albums, many=True)
        return Response(serializer.data)
