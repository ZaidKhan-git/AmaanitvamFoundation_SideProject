"""
Email Service Module for Amaanitvam Foundation

This module handles sending emails for various purposes,
primarily donation receipts after successful payments.
"""

import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


def send_donation_receipt(donation):
    """
    Send a donation receipt email to the donor.
    
    Args:
        donation: Donation model instance with the following attributes:
            - donor_name: Name of the donor
            - donor_email: Email address of the donor
            - amount: Donation amount
            - transaction_id: Razorpay payment ID
            - razorpay_order_id: Razorpay order ID
            - date: Donation date
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Prepare context for email template
        context = {
            'donor_name': donation.donor_name,
            'amount': donation.amount,
            'transaction_id': donation.transaction_id or 'N/A',
            'order_id': donation.razorpay_order_id or 'N/A',
            'donation_date': timezone.localtime(donation.date).strftime('%B %d, %Y at %I:%M %p'),
        }
        
        # Subject line
        subject = f'Thank You for Your Donation of ₹{donation.amount} - Amaanitvam Foundation'
        
        # Render HTML email template
        html_content = render_to_string('emails/email_donation_receipt.html', context)
        
        # Create plain text version for email clients that don't support HTML
        plain_text_content = f"""
Dear {donation.donor_name},

Thank you for your generous donation of ₹{donation.amount} to Amaanitvam Foundation!

DONATION RECEIPT
================
Amount: ₹{donation.amount}
Transaction ID: {context['transaction_id']}
Order ID: {context['order_id']}
Date: {context['donation_date']}

80G TAX EXEMPTION
================
Your donation is eligible for tax deduction under Section 80G of the Income Tax Act.
The official 80G certificate will be sent to you within 7 working days.

Your contribution helps us provide education, nutrition, and healthcare to 
underprivileged children. Every rupee you contribute makes a difference!

Thank you for being a part of our mission.

With gratitude,
Amaanitvam Foundation

---
Email: amaanitvamfoundation@gmail.com
Website: www.amaanitvamfoundation.org
        """
        
        # Get donor email
        donor_email = getattr(donation, 'donor_email', None)
        if not donor_email:
            logger.error(f"No donor email found for donation ID: {donation.id}")
            return False
        
        # Create email message with both HTML and plain text versions
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[donor_email],
            reply_to=['amaanitvamfoundation@gmail.com'],
        )
        
        # Attach HTML version
        email.attach_alternative(html_content, "text/html")
        
        # Send the email
        email.send(fail_silently=False)
        
        logger.info(f"Donation receipt email sent successfully to {donor_email} for donation ID: {donation.id}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send donation receipt email for donation ID: {donation.id}. Error: {str(e)}")
        return False


def send_test_email(to_email):
    """
    Send a test email to verify email configuration.
    
    Args:
        to_email: Email address to send test email to
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        email = EmailMultiAlternatives(
            subject='Test Email - Amaanitvam Foundation',
            body='This is a test email to verify email configuration is working correctly.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.send(fail_silently=False)
        logger.info(f"Test email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send test email to {to_email}. Error: {str(e)}")
        return False
