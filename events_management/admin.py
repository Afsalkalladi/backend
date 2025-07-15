from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Event, EventRegistration, EventSpeaker, EventSchedule, EventFeedback


class EventSpeakerInline(admin.TabularInline):
    model = EventSpeaker
    extra = 1
    fields = ('name', 'title', 'organization', 'talk_title', 'order')


class EventScheduleInline(admin.TabularInline):
    model = EventSchedule
    extra = 1
    fields = ('title', 'speaker', 'start_time', 'end_time', 'venue_details')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'status', 'registration_count', 'spots_remaining', 'created_by')
    list_filter = ('event_type', 'status', 'is_online', 'is_free', 'created_by')
    search_fields = ('title', 'description', 'venue')
    readonly_fields = ('registration_count', 'spots_remaining', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'event_type', 'status')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date', 'registration_deadline')
        }),
        ('Location', {
            'fields': ('venue', 'address', 'is_online', 'meeting_link')
        }),
        ('Registration Settings', {
            'fields': ('max_participants', 'registration_fee', 'is_free', 'registration_count', 'spots_remaining')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone')
        }),
        ('Media', {
            'fields': ('banner_image', 'event_flyer')
        }),
        ('Management', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [EventSpeakerInline, EventScheduleInline]
    
    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def registration_count(self, obj):
        return obj.registration_count
    registration_count.short_description = 'Registrations'
    
    def spots_remaining(self, obj):
        remaining = obj.spots_remaining
        if remaining == "Unlimited":
            return format_html('<span style="color: green;">Unlimited</span>')
        elif remaining == 0:
            return format_html('<span style="color: red;">Full</span>')
        else:
            return format_html('<span style="color: orange;">{}</span>', remaining)
    spots_remaining.short_description = 'Spots Left'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'payment_status', 'payment_amount', 'attended', 'registered_at')
    list_filter = ('payment_status', 'attended', 'certificate_issued', 'event__event_type')
    search_fields = ('name', 'email', 'event__title', 'institution', 'organization')
    readonly_fields = ('registered_at', 'updated_at')
    
    fieldsets = (
        ('Event', {
            'fields': ('event',)
        }),
        ('Personal Information', {
            'fields': ('name', 'email', 'mobile_number')
        }),
        ('Academic Information', {
            'fields': ('institution', 'department', 'year_of_study')
        }),
        ('Professional Information', {
            'fields': ('organization', 'designation')
        }),
        ('Payment Information', {
            'fields': ('payment_status', 'payment_amount', 'payment_verified_by', 'payment_date', 'payment_reference')
        }),
        ('Additional Information', {
            'fields': ('dietary_requirements', 'special_needs')
        }),
        ('Attendance', {
            'fields': ('attended', 'certificate_issued')
        }),
        ('Metadata', {
            'fields': ('registered_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_paid', 'mark_as_attended', 'issue_certificates']
    
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(
            payment_status='paid',
            payment_verified_by=request.user,
            payment_date=timezone.now()
        )
        self.message_user(request, f'{updated} registration(s) marked as paid')
    mark_as_paid.short_description = 'Mark selected registrations as paid'
    
    def mark_as_attended(self, request, queryset):
        updated = queryset.update(attended=True)
        self.message_user(request, f'{updated} registration(s) marked as attended')
    mark_as_attended.short_description = 'Mark selected registrations as attended'
    
    def issue_certificates(self, request, queryset):
        updated = queryset.filter(attended=True).update(certificate_issued=True)
        self.message_user(request, f'{updated} certificate(s) issued')
    issue_certificates.short_description = 'Issue certificates to attended participants'


@admin.register(EventSpeaker)
class EventSpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'organization', 'event', 'talk_title', 'order')
    list_filter = ('event', 'organization')
    search_fields = ('name', 'title', 'organization', 'talk_title')
    ordering = ('event', 'order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('event', 'name', 'title', 'organization', 'bio', 'profile_image')
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'twitter_url', 'website_url')
        }),
        ('Talk Details', {
            'fields': ('talk_title', 'talk_abstract', 'talk_duration', 'order')
        }),
    )


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'speaker', 'start_time', 'end_time', 'venue_details')
    list_filter = ('event',)
    search_fields = ('title', 'event__title', 'speaker__name')
    ordering = ('event', 'start_time')


@admin.register(EventFeedback)
class EventFeedbackAdmin(admin.ModelAdmin):
    list_display = ('event', 'registration', 'overall_rating', 'content_rating', 'organization_rating', 'would_recommend', 'submitted_at')
    list_filter = ('overall_rating', 'content_rating', 'organization_rating', 'would_recommend', 'event')
    search_fields = ('event__title', 'registration__name', 'liked_most', 'improvements')
    readonly_fields = ('submitted_at',)
    
    fieldsets = (
        ('Event & Participant', {
            'fields': ('event', 'registration')
        }),
        ('Ratings', {
            'fields': ('overall_rating', 'content_rating', 'organization_rating')
        }),
        ('Comments', {
            'fields': ('liked_most', 'improvements', 'additional_comments')
        }),
        ('Recommendations', {
            'fields': ('would_recommend', 'future_topics')
        }),
        ('Metadata', {
            'fields': ('submitted_at',)
        }),
    )
