from django.contrib import admin
from django.utils.html import format_html
from .models import StoryPost, StoryImage, Donation, VolunteerFormLink, SiteContent, Project, ProjectImage, ProjectUpdate, StaticMedia


class StoryImageInline(admin.TabularInline):
    """Inline admin for adding multiple images to a story."""
    model = StoryImage
    extra = 1  # Show 1 empty row by default
    max_num = 6  # Limit to 6 images per story
    ordering = ['order']
    fields = ['image', 'caption', 'order']


@admin.register(StoryPost)
class StoryPostAdmin(admin.ModelAdmin):
    """Admin configuration for Story Posts."""
    
    list_display = [
        'title',
        'category',
        'is_published',
        'has_video',
        'created_date',
    ]
    list_filter = ['category', 'is_published', 'created_date']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    
    inlines = [StoryImageInline]
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'body', 'category')
        }),
        ('Media', {
            'fields': ('cover_image', 'video_url', 'video_file'),
            'description': 'Add a cover image and/or video. Videos will autoplay when users view the story. Additional story images can be added below.'
        }),
        ('Publishing', {
            'fields': ('is_published',)
        }),
    )

    def has_video(self, obj):
        """Display if story has video content."""
        return obj.has_video()
    has_video.boolean = True
    has_video.short_description = 'Has Video'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    """Admin configuration for Donations."""
    
    list_display = [
        'donor_name',
        'donor_email',
        'amount_display',
        'status',
        'created_at',
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'donor_phone', 'transaction_id']
    readonly_fields = [
        'transaction_id',
        'razorpay_order_id',
        'razorpay_signature',
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone')
        }),
        ('Payment Details', {
            'fields': ('amount', 'status')
        }),
        ('Razorpay Details (Read-only)', {
            'fields': ('transaction_id', 'razorpay_order_id', 'razorpay_signature'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def amount_display(self, obj):
        """Display amount with currency symbol."""
        return f"₹{obj.amount}"
    amount_display.short_description = 'Amount'
    amount_display.admin_order_field = 'amount'


@admin.register(VolunteerFormLink)
class VolunteerFormLinkAdmin(admin.ModelAdmin):
    """Admin configuration for Volunteer Form Links."""
    
    list_display = [
        'title',
        'is_active',
        'form_url_display',
        'updated_at',
    ]
    list_filter = ['is_active']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Form Configuration', {
            'fields': ('title', 'form_url', 'is_active'),
            'description': 'Add your volunteer recruitment form URL here. Toggle "Is active" to enable/disable the form link.'
        }),
        ('Disclaimer Message', {
            'fields': ('disclaimer_message',),
            'description': 'This message is shown when volunteer recruitment is not active.'
        }),
    )

    def form_url_display(self, obj):
        """Display truncated URL."""
        url = obj.form_url
        if len(url) > 50:
            return f"{url[:50]}..."
        return url
    form_url_display.short_description = 'Form URL'


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    """Admin configuration for Site Content (editable website content)."""
    
    list_display = ['label', 'page', 'section', 'content_type', 'content_preview']
    list_filter = ['page', 'section', 'content_type']
    search_fields = ['key', 'label', 'text_content']
    ordering = ['page', 'section', 'key']
    
    fieldsets = (
        ('Identification', {
            'fields': ('key', 'page', 'section', 'label'),
            'description': 'Unique key identifies this content. Page and section help organize content.'
        }),
        ('Content', {
            'fields': ('content_type', 'text_content', 'image_content'),
            'description': 'Enter text/HTML content OR upload an image based on content type.'
        }),
    )
    
    def content_preview(self, obj):
        """Show a preview of the content."""
        if obj.content_type == 'image' and obj.image_content:
            return "📷 Image uploaded"
        content = obj.text_content
        if len(content) > 50:
            return f"{content[:50]}..."
        return content or "—"
    content_preview.short_description = 'Preview'


class ProjectImageInline(admin.TabularInline):
    """Inline admin for adding gallery images to a project."""
    model = ProjectImage
    extra = 1
    max_num = 6  # Limit to 6 images per project
    ordering = ['order']
    fields = ['image', 'caption', 'order']


class ProjectUpdateInline(admin.StackedInline):
    """Inline admin for adding updates to a project."""
    model = ProjectUpdate
    extra = 0
    ordering = ['-date']
    fields = ['title', 'date', 'content']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Admin configuration for Projects."""
    
    list_display = [
        'title',
        'status',
        'location',
        'beneficiaries_count',
        'is_active',
        'updated_at',
    ]
    list_filter = ['status', 'is_active', 'created_at']
    list_editable = ['is_active', 'status']
    search_fields = ['title', 'short_description', 'full_description', 'location']
    prepopulated_fields = {'slug': ('title',)}
    
    inlines = [ProjectImageInline, ProjectUpdateInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'status', 'is_active'),
            'description': 'Enter the project title and set its status.'
        }),
        ('Descriptions', {
            'fields': ('short_description', 'full_description'),
            'description': 'Short description appears on cards, full description on the detail page.'
        }),
        ('Media', {
            'fields': ('cover_image', 'video_url'),
            'description': 'Upload a cover image. Gallery images can be added below.'
        }),
        ('Details', {
            'fields': ('location', 'beneficiaries_count'),
            'description': 'Project location and impact metrics.'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('images', 'updates')


@admin.register(StaticMedia)
class StaticMediaAdmin(admin.ModelAdmin):
    """Admin configuration for Static Media (images and videos)."""
    
    list_display = ['location_display', 'media_type', 'is_active', 'media_preview', 'updated_at']
    list_filter = ['media_type', 'is_active']
    list_editable = ['is_active']
    search_fields = ['location', 'label', 'alt_text']
    ordering = ['location']
    readonly_fields = ['key', 'media_preview_large', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Location', {
            'fields': ('location', 'key', 'label'),
            'description': 'Select where this media will appear on the website.'
        }),
        ('Media Upload', {
            'fields': ('media_type', 'image', 'video', 'alt_text'),
            'description': 'Upload an image OR video based on the media type. Use high-quality images for best results.'
        }),
        ('Status', {
            'fields': ('is_active',),
            'description': 'Toggle to enable/disable this media. When disabled, fallback images will be used.'
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Only show preview and timestamps for existing objects."""
        if obj:  # Editing existing object
            return ['key', 'media_preview_large', 'created_at', 'updated_at']
        return ['key']  # New object - no preview yet
    
    def get_fieldsets(self, request, obj=None):
        """Only show preview section for existing objects."""
        fieldsets = [
            ('Location', {
                'fields': ('location', 'key', 'label'),
                'description': 'Select where this media will appear on the website.'
            }),
            ('Media Upload', {
                'fields': ('media_type', 'image', 'video', 'alt_text'),
                'description': 'Upload an image OR video based on the media type. Use high-quality images for best results.'
            }),
            ('Status', {
                'fields': ('is_active',),
                'description': 'Toggle to enable/disable this media. When disabled, fallback images will be used.'
            }),
        ]
        if obj:  # Only show preview for existing objects
            fieldsets.insert(2, ('Preview', {
                'fields': ('media_preview_large',),
                'classes': ('collapse',)
            }))
            fieldsets.append(('Timestamps', {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',)
            }))
        return fieldsets
    
    def location_display(self, obj):
        """Display the human-readable location name."""
        if obj and obj.location:
            return obj.get_location_display()
        return "—"
    location_display.short_description = 'Location'
    location_display.admin_order_field = 'location'
    
    def media_preview(self, obj):
        """Show small preview thumbnail in list view."""
        if obj.media_type == 'image' and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 80px; max-height: 50px; object-fit: cover; border-radius: 4px;"/>',
                obj.image.url
            )
        elif obj.media_type == 'video' and obj.video:
            return format_html(
                '<span style="color: #666; font-size: 11px;">🎬 Video uploaded</span>'
            )
        return format_html('<span style="color: #999;">No media</span>')
    media_preview.short_description = 'Preview'
    
    def media_preview_large(self, obj):
        """Show larger preview in detail view."""
        if not obj or not obj.pk:
            return "Save first to see preview"
        if obj.media_type == 'image' and obj.image:
            return format_html(
                '<img src="{}" style="max-width: 400px; max-height: 300px; object-fit: contain; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        elif obj.media_type == 'video' and obj.video:
            return format_html(
                '<video controls style="max-width: 400px; max-height: 300px; border-radius: 8px;"><source src="{}" type="video/mp4">Your browser does not support video.</video>',
                obj.video.url
            )
        return "No media uploaded yet"
    media_preview_large.short_description = 'Current Media'
