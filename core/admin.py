from django.contrib import admin
from .models import StoryPost, Donation


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
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'body', 'category')
        }),
        ('Media', {
            'fields': ('cover_image', 'video_url', 'video_file'),
            'description': 'Add a cover image and/or video. Videos will autoplay when users view the story.'
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
