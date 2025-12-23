from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class StoryPost(models.Model):
    """
    Model for managing stories/blog posts about the foundation's work.
    Supports optional video (with autoplay) and cover images.
    """
    CATEGORY_CHOICES = [
        ('education', 'Education'),
        ('health', 'Health'),
        ('food', 'Food'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    body = models.TextField(help_text="Main content of the story (supports HTML)")
    
    # Media fields - both optional
    cover_image = models.ImageField(
        upload_to='stories/images/',
        blank=True,
        null=True,
        help_text="Cover image for the story"
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube/Vimeo URL or direct video link. Will autoplay on story page."
    )
    video_file = models.FileField(
        upload_to='stories/videos/',
        blank=True,
        null=True,
        help_text="Upload video directly (MP4 recommended). Will autoplay on story page."
    )
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='education'
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_date']
        verbose_name = "Story Post"
        verbose_name_plural = "Story Posts"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('story_detail', kwargs={'slug': self.slug})

    def has_video(self):
        """Check if the story has any video content."""
        return bool(self.video_url or self.video_file)

    def get_embed_url(self):
        """
        Convert YouTube/Vimeo URLs to embed format for autoplay.
        Returns None if video_file is used instead.
        """
        if not self.video_url:
            return None
        
        url = self.video_url
        
        # YouTube handling
        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[1].split('&')[0]
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1"
        elif 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[1].split('?')[0]
            return f"https://www.youtube.com/embed/{video_id}?autoplay=1&mute=1"
        
        # Vimeo handling
        elif 'vimeo.com/' in url:
            video_id = url.split('vimeo.com/')[1].split('?')[0]
            return f"https://player.vimeo.com/video/{video_id}?autoplay=1&muted=1"
        
        # Direct video URL - use HTML5 player
        return None


class Donation(models.Model):
    """
    Model for tracking all incoming donations via Razorpay.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    # Razorpay transaction details
    transaction_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Razorpay Payment ID"
    )
    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Razorpay Order ID"
    )
    razorpay_signature = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Razorpay Signature for verification"
    )

    # Donor information
    donor_name = models.CharField(max_length=100)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=15)
    
    # Donation details
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount in INR"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    def __str__(self):
        return f"{self.donor_name} - ₹{self.amount} ({self.status})"

    @property
    def amount_in_paise(self):
        """Convert amount to paise for Razorpay."""
        return int(self.amount * 100)
