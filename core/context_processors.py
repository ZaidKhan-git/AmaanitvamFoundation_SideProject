"""
Context processors for making site content available in all templates.
"""


def site_content(request):
    """
    Make all site content available in templates via the 'site' variable.
    Usage in templates: {{ site.key_name }} or {{ site.key_name.url }} for images
    """
    from .models import SiteContent
    
    content = {}
    for item in SiteContent.objects.all():
        if item.content_type == 'image':
            content[item.key] = item.image_content
        else:
            content[item.key] = item.text_content
    
    return {'site': content}


def static_media(request):
    """
    Make all static media available in templates via the 'media' variable.
    Usage in templates: 
        {{ media.home_hero_bg }} - returns URL string or None
        {{ media.home_hero_bg_obj }} - returns the StaticMedia object
    """
    from .models import StaticMedia
    
    media = {}
    for item in StaticMedia.objects.filter(is_active=True):
        # Store the URL for easy access
        media[item.location] = item.get_url()
        # Also store the object for access to alt_text and other fields
        media[f"{item.location}_obj"] = item
    
    return {'media': media}
