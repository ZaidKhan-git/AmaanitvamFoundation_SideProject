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


class StoryImage(models.Model):
    """
    Additional images for a story post.
    Displayed in alternating left/right layout with content.
    """
    story = models.ForeignKey(
        StoryPost,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='stories/images/',
        help_text="Image to display in the story"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional caption for the image"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which images appear (lower = earlier)"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Story Image"
        verbose_name_plural = "Story Images"

    def __str__(self):
        return f"Image {self.order + 1} for {self.story.title}"


class Donation(models.Model):
    """
    Model for tracking all incoming donations via Razorpay.
    """
    name = models.CharField(max_length=100)
    amount = models.CharField(max_length=100, help_text="Amount in INR")
    payment_id = models.CharField(max_length=100) # Razorpay Payment ID
    order_id = models.CharField(max_length=100, unique=True) # Razorpay Order ID
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    def __str__(self):
        return f"{self.name} - ₹{self.amount} ({'Paid' if self.paid else 'Pending'})"


class VolunteerFormLink(models.Model):
    """
    Model for managing volunteer recruitment form links.
    Admin can add/update the form link, and toggle whether recruitment is active.
    """
    title = models.CharField(
        max_length=100,
        default="Volunteer Application Form",
        help_text="Title displayed in admin (for reference)"
    )
    form_url = models.URLField(
        help_text="Google Form or other form URL for volunteer applications"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="When active, the Apply button links to this form. When inactive, a disclaimer popup is shown."
    )
    disclaimer_message = models.TextField(
        default="Volunteer recruitment is currently closed. Please check back later or follow us on social media for updates.",
        help_text="Message shown when no active recruitment is available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Volunteer Form Link"
        verbose_name_plural = "Volunteer Form Links"
        ordering = ['-updated_at']

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return f"{self.title} ({status})"

    @classmethod
    def get_active_link(cls):
        """Get the currently active volunteer form link, if any."""
        return cls.objects.filter(is_active=True).first()


class SiteContent(models.Model):
    """
    Flexible key-value content storage for editable website content.
    Allows admin to edit text, images, and URLs across all pages.
    """
    PAGE_CHOICES = [
        ('home', 'Home Page'),
        ('about', 'About Page'),
        ('what_we_do', 'What We Do'),
        ('ways_to_help', 'Ways to Help'),
        ('donate', 'Donate Page'),
        ('stories', 'Stories Page'),
    ]
    CONTENT_TYPE_CHOICES = [
        ('text', 'Plain Text'),
        ('html', 'Rich Text (HTML)'),
        ('image', 'Image'),
        ('url', 'External URL'),
    ]
    
    key = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique identifier (e.g., home_hero_title)"
    )
    page = models.CharField(
        max_length=50,
        choices=PAGE_CHOICES,
        help_text="Which page this content belongs to"
    )
    section = models.CharField(
        max_length=100,
        help_text="Section name (e.g., Hero, Mission, CTA)"
    )
    label = models.CharField(
        max_length=200,
        help_text="Human-readable description of this content"
    )
    content_type = models.CharField(
        max_length=20,
        choices=CONTENT_TYPE_CHOICES,
        default='text'
    )
    text_content = models.TextField(
        blank=True,
        help_text="Text or HTML content"
    )
    image_content = models.ImageField(
        upload_to='site_content/',
        blank=True,
        null=True,
        help_text="Image file (for image content type)"
    )
    
    class Meta:
        verbose_name = "Site Content"
        verbose_name_plural = "Site Content"
        ordering = ['page', 'section', 'key']
    
    def __str__(self):
        return f"{self.label} ({self.page})"
    
    def get_content(self):
        """Return the appropriate content based on type."""
        if self.content_type == 'image':
            return self.image_content
        return self.text_content


class Project(models.Model):
    """
    Model for managing education projects.
    Each project can have a cover image, gallery images, video, and updates.
    """
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('upcoming', 'Upcoming'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    short_description = models.CharField(
        max_length=300,
        help_text="Brief description shown on project card (max 300 chars)"
    )
    full_description = models.TextField(
        help_text="Detailed description of the project (supports HTML)"
    )
    
    # Cover image (main image)
    cover_image = models.ImageField(
        upload_to='projects/covers/',
        help_text="Main cover image for the project"
    )
    
    # Optional video
    video_url = models.URLField(
        blank=True,
        null=True,
        help_text="YouTube/Vimeo URL for project video"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ongoing'
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Show this project on the website"
    )
    
    # Location/area
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Project location (e.g., 'Mehrauli, Delhi')"
    )
    
    # Beneficiaries count
    beneficiaries_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of children/beneficiaries impacted"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Project"
        verbose_name_plural = "Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})
    
    def latest_update(self):
        """Get the most recent update for this project."""
        return self.updates.first()


class ProjectImage(models.Model):
    """
    Gallery images for a project (5-6 images per project).
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='projects/gallery/',
        help_text="Gallery image for the project"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional caption for the image"
    )
    order = models.PositiveIntegerField(
        default=0,
        help_text="Order in which images appear (lower = first)"
    )
    
    class Meta:
        ordering = ['order']
        verbose_name = "Project Image"
        verbose_name_plural = "Project Images"
    
    def __str__(self):
        return f"Image {self.order + 1} for {self.project.title}"


class ProjectUpdate(models.Model):
    """
    Latest updates/news for a project.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='updates'
    )
    title = models.CharField(max_length=200)
    content = models.TextField(help_text="Update content (supports HTML)")
    date = models.DateField(help_text="Date of the update")
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Project Update"
        verbose_name_plural = "Project Updates"
    
    def __str__(self):
        return f"{self.title} ({self.project.title})"


class StaticMedia(models.Model):
    """
    Model for managing static images and videos used throughout the website.
    Allows admin to update hero backgrounds, logos, impact photos, etc.
    """
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    LOCATION_CHOICES = [
        # Home Page
        ('home_hero_bg', 'Home - Hero Background'),
        ('home_impact_1', 'Home - Impact Photo 1'),
        ('home_impact_2', 'Home - Impact Photo 2'),
        ('home_impact_3', 'Home - Impact Photo 3'),
        ('home_impact_4', 'Home - Impact Photo 4'),
        ('home_impact_5', 'Home - Impact Photo 5'),
        ('home_impact_6', 'Home - Impact Photo 6'),
        ('home_impact_7', 'Home - Impact Photo 7'),
        ('home_impact_8', 'Home - Impact Photo 8'),
        ('home_placeholder_1', 'Home - Placeholder Story 1'),
        ('home_placeholder_2', 'Home - Placeholder Story 2'),
        ('home_placeholder_3', 'Home - Placeholder Story 3'),
        # About Page
        ('about_hero_bg', 'About - Hero Background'),
        # What We Do Page
        ('whatwedo_hero_bg', 'What We Do - Hero Background'),
        ('whatwedo_mission_1', 'What We Do - Mission Image 1'),
        ('whatwedo_mission_2', 'What We Do - Mission Image 2'),
        # Ways to Help Page
        ('waystohelp_hero_bg', 'Ways to Help - Hero Background'),
        # Donate Page
        ('donate_hero_bg', 'Donate - Hero Background'),
        # Stories Page
        ('stories_hero_video', 'Stories - Hero Video'),
        # Site-wide
        ('navbar_logo', 'Navbar Logo'),
        ('footer_logo', 'Footer Logo'),
    ]
    
    key = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique identifier for this media (auto-filled from location)"
    )
    location = models.CharField(
        max_length=50,
        choices=LOCATION_CHOICES,
        unique=True,
        help_text="Where this media appears on the website"
    )
    label = models.CharField(
        max_length=200,
        help_text="Human-readable description of this media"
    )
    media_type = models.CharField(
        max_length=10,
        choices=MEDIA_TYPE_CHOICES,
        default='image'
    )
    image = models.ImageField(
        upload_to='static_media/',
        blank=True,
        null=True,
        help_text="Upload image (JPG, PNG, WebP recommended)"
    )
    video = models.FileField(
        upload_to='static_media/videos/',
        blank=True,
        null=True,
        help_text="Upload video file (MP4 recommended)"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alt text for accessibility"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="When inactive, fallback/default media will be used"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Static Media"
        verbose_name_plural = "Static Media"
        ordering = ['location']
    
    def __str__(self):
        if self.location:
            return f"{self.get_location_display()}"
        return "New Static Media"
    
    def save(self, *args, **kwargs):
        # Delete old files when updating with new ones
        if self.pk:
            try:
                old_instance = StaticMedia.objects.get(pk=self.pk)
                # Check if image is being replaced
                if old_instance.image and self.image and old_instance.image != self.image:
                    old_instance.image.delete(save=False)
                # Check if video is being replaced
                if old_instance.video and self.video and old_instance.video != self.video:
                    old_instance.video.delete(save=False)
            except StaticMedia.DoesNotExist:
                pass
        
        # Auto-fill key from location if not set
        if self.location and not self.key:
            self.key = self.location
        # Auto-fill label from location display name
        if self.location and not self.label:
            self.label = self.get_location_display()
        super().save(*args, **kwargs)
    
    def get_url(self):
        """Return the URL for the media file."""
        if self.media_type == 'video' and self.video:
            return self.video.url
        elif self.image:
            return self.image.url
        return None
    
    @classmethod
    def get_media(cls, location_key):
        """Get active media for a specific location."""
        try:
            media = cls.objects.get(location=location_key, is_active=True)
            return media.get_url()
        except cls.DoesNotExist:
            return None
