from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json

from .models import StoryPost, Donation, VolunteerFormLink, Project


# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def home(request):
    """
    Homepage with hero section, impact metrics, and latest stories.
    """
    # Get latest 3 published stories for the homepage
    latest_stories = StoryPost.objects.filter(is_published=True)[:3]
    
    # Impact metrics (these can be made dynamic later)
    impact_metrics = {
        'children_helped': 5000,
        'meals_served': 25000,
        'schools_supported': 15,
    }
    
    context = {
        'latest_stories': latest_stories,
        'impact_metrics': impact_metrics,
    }
    return render(request, 'home.html', context)


def about(request):
    """
    About page with foundation information.
    """
    return render(request, 'about.html')


def what_we_do(request):
    """
    What We Do page - details about programs and initiatives.
    """
    # Get active projects with their latest updates
    projects = Project.objects.filter(is_active=True).prefetch_related('images', 'updates')
    
    context = {
        'projects': projects,
    }
    return render(request, 'what_we_do.html', context)


def project_detail(request, slug):
    """
    Project detail page - shows all images and updates for a project.
    """
    project = get_object_or_404(Project, slug=slug, is_active=True)
    
    context = {
        'project': project,
        'images': project.images.all(),
        'updates': project.updates.all(),
    }
    return render(request, 'project_detail.html', context)


def ways_to_help(request):
    """
    Ways to Help page - different ways to contribute.
    Includes volunteer form link functionality.
    """
    # Get active volunteer form link
    volunteer_link = VolunteerFormLink.get_active_link()
    
    # Get disclaimer message (from most recent entry or default)
    if volunteer_link:
        disclaimer_message = volunteer_link.disclaimer_message
        volunteer_form_url = volunteer_link.form_url
        volunteer_active = True
    else:
        # Check if there's any entry to get the disclaimer from
        any_link = VolunteerFormLink.objects.first()
        disclaimer_message = any_link.disclaimer_message if any_link else "Volunteer recruitment is currently closed. Please check back later or follow us on social media for updates."
        volunteer_form_url = None
        volunteer_active = False
    
    context = {
        'volunteer_form_url': volunteer_form_url,
        'volunteer_active': volunteer_active,
        'disclaimer_message': disclaimer_message,
    }
    return render(request, 'ways_to_help.html', context)


def stories_list(request):
    """
    Grid layout of all published stories.
    """
    stories = StoryPost.objects.filter(is_published=True)
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        stories = stories.filter(category=category)
    
    context = {
        'stories': stories,
        'categories': StoryPost.CATEGORY_CHOICES,
        'selected_category': category,
    }
    return render(request, 'stories_list.html', context)


def story_detail(request, slug):
    """
    Individual story page with video autoplay support.
    """
    story = get_object_or_404(StoryPost, slug=slug, is_published=True)
    
    # Get related stories (same category, excluding current)
    related_stories = StoryPost.objects.filter(
        category=story.category,
        is_published=True
    ).exclude(id=story.id)[:3]
    
    context = {
        'story': story,
        'related_stories': related_stories,
    }
    return render(request, 'story_detail.html', context)


@csrf_exempt  # Exempt for ngrok mobile testing - remove in production
def donate(request):
    """
    Donation page with Razorpay integration.
    """
    if request.method == 'POST':
        # Get form data
        donor_name = request.POST.get('donor_name')
        donor_email = request.POST.get('donor_email')
        donor_phone = request.POST.get('donor_phone')
        amount = request.POST.get('amount')
        
        # Input validation: reject zero or negative amounts
        try:
            if int(float(amount)) < 1:
                return HttpResponse("Invalid Amount", status=400)
        except (ValueError, TypeError):
            return HttpResponse("Invalid Amount", status=400)
        
        try:
            amount_decimal = float(amount)
            amount_paise = int(amount_decimal * 100)
            
            # Create Razorpay order
            order_data = {
                'amount': amount_paise,
                'currency': settings.RAZORPAY_CURRENCY,
                'receipt': f'donation_{donor_email}',
                'payment_capture': 1  # Auto capture
            }
            razorpay_order = razorpay_client.order.create(order_data)
            
            # Create donation record with pending status
            donation = Donation.objects.create(
                razorpay_order_id=razorpay_order['id'],
                donor_name=donor_name,
                donor_email=donor_email,
                donor_phone=donor_phone,
                amount=amount_decimal,
                status='pending'
            )
            
            context = {
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': amount_paise,
                'amount_display': amount_decimal,
                'currency': settings.RAZORPAY_CURRENCY,
                'donor_name': donor_name,
                'donor_email': donor_email,
                'donor_phone': donor_phone,
                'donation_id': donation.id,
            }
            return render(request, 'donate_checkout.html', context)
            
        except Exception as e:
            context = {
                'error': str(e),
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            }
            return render(request, 'donate.html', context)
    
    context = {
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'donate.html', context)


@csrf_exempt
def payment_callback(request):
    """
    Handle Razorpay payment callback and verify signature.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            razorpay_order_id = data.get('razorpay_order_id')
            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')
            
            # Verify signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }
            
            try:
                razorpay_client.utility.verify_payment_signature(params_dict)
                
                # Update donation record
                donation = Donation.objects.get(razorpay_order_id=razorpay_order_id)
                donation.transaction_id = razorpay_payment_id
                donation.razorpay_signature = razorpay_signature
                donation.status = 'success'
                donation.save()
                
                return JsonResponse({'status': 'success', 'donation_id': donation.id})
                
            except razorpay.errors.SignatureVerificationError:
                # Update donation as failed
                donation = Donation.objects.get(razorpay_order_id=razorpay_order_id)
                donation.status = 'failed'
                donation.save()
                
                return JsonResponse({'status': 'failed', 'error': 'Signature verification failed'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)})
    
    return JsonResponse({'status': 'error', 'error': 'Invalid request method'})


def payment_success(request):
    """
    Thank you page after successful donation.
    """
    donation_id = request.GET.get('donation_id')
    donation = None
    
    if donation_id:
        try:
            donation = Donation.objects.get(id=donation_id, status='success')
        except Donation.DoesNotExist:
            pass
    
    context = {
        'donation': donation,
    }
    return render(request, 'payment_success.html', context)


def payment_failed(request):
    """
    Page shown when payment fails.
    """
    return render(request, 'payment_failed.html')


def privacy_policy(request):
    """
    Privacy Policy page - required for Razorpay compliance.
    """
    return render(request, 'privacy.html')


def terms_conditions(request):
    """
    Terms & Conditions page - required for Razorpay compliance.
    """
    return render(request, 'terms.html')


def refund_policy(request):
    """
    Refund Policy page - required for Razorpay compliance.
    """
    return render(request, 'refund.html')
