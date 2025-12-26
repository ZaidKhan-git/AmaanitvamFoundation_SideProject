from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('who-we-are/', views.about, name='about'),
    path('what-we-do/', views.what_we_do, name='what_we_do'),
    path('ways-to-help/', views.ways_to_help, name='ways_to_help'),
    
    # Stories/Blog
    path('stories/', views.stories_list, name='stories_list'),
    path('stories/<slug:slug>/', views.story_detail, name='story_detail'),
    
    # Projects
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    
    # Donations
    path('donate/', views.donate, name='donate'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failed/', views.payment_failed, name='payment_failed'),
    
    # Legal Pages (Razorpay Compliance)
    path('privacy-policy/', views.privacy_policy, name='privacy'),
    path('terms-conditions/', views.terms_conditions, name='terms'),
    path('refund-policy/', views.refund_policy, name='refund'),
]
