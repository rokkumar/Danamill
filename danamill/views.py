"""
Views for danamill project.
Handles all main site pages and contact form submission.
"""

import json
import logging
import re
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.http import require_http_methods
from .services import send_contact_email


# ============================================================
# LOGGER
# ============================================================

logger = logging.getLogger(__name__)


# ============================================================
# HOME VIEW
# ============================================================

def home(request):
    """Homepage view"""
    return render(request, 'home.html')


# ============================================================
# ABOUT VIEW
# ============================================================

def about(request):
    """About Us page"""
    return render(request, 'about.html')


# ============================================================
# QUALITY VIEW
# ============================================================

def quality(request):
    """Quality page (main site)"""
    return render(request, 'quality.html')


# ============================================================
# PRODUCTS VIEW
# ============================================================

def products(request):
    """Products listing page"""
    return render(request, 'products.html')


# ============================================================
# INFRASTRUCTURE VIEW
# ============================================================

def infrastructure(request):
    """Infrastructure page"""
    return render(request, 'infrastructure.html')


# ============================================================
# CART VIEW
# ============================================================

def cart(request):
    """Shopping cart page"""
    return render(request, 'cart.html')


# ============================================================
# CONTACT VIEW (with form handling + email service + honeypot)
# ============================================================

@require_http_methods(["GET", "POST"])
def contact(request):
    """
    Contact page with form handling.
    
    GET  → Render contact page
    POST → Validate form, check honeypot, call email service, return JSON response
    """
    
    if request.method == 'POST':
        try:
            # ------------------------------------------
            # Parse incoming data (JSON or Form)
            # ------------------------------------------
            if request.content_type == 'application/json':
                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError:
                    return JsonResponse({
                        'success': False,
                        'message': 'Invalid JSON format.'
                    }, status=400)
            else:
                data = request.POST.dict()

            # ------------------------------------------
            # Honeypot check (Spam bot protection)
            # ------------------------------------------
            if data.get('website'):
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you! We will contact you soon.'
                })

            # ------------------------------------------
            # Extract fields
            # ------------------------------------------
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            phone = data.get('phone', '').strip()
            subject = data.get('subject', '').strip()
            message = data.get('message', '').strip()

            # ------------------------------------------
            # Validation
            # ------------------------------------------
            errors = {}

            if not name:
                errors['name'] = 'Please enter your full name.'
            elif len(name) < 2:
                errors['name'] = 'Name must be at least 2 characters.'

            if not email:
                errors['email'] = 'Please enter your email address.'
            elif '@' not in email or '.' not in email:
                errors['email'] = 'Please enter a valid email address.'

            if not phone:
                errors['phone'] = 'Please enter your phone number.'
            else:
                # Remove spaces, dashes, brackets for validation
                digits = ''.join(filter(str.isdigit, phone))
                if len(digits) < 10:
                    errors['phone'] = 'Please enter a valid 10-digit phone number.'

            if not subject:
                errors['subject'] = 'Please enter a subject.'
            elif len(subject) < 3:
                errors['subject'] = 'Subject must be at least 3 characters.'

            if not message:
                errors['message'] = 'Please enter your message.'
            elif len(message) < 10:
                errors['message'] = 'Message must be at least 10 characters.'

            # ------------------------------------------
            # Return validation errors
            # ------------------------------------------
            if errors:
                logger.warning(f"Contact form validation errors: {errors}")
                return JsonResponse({
                    'success': False,
                    'message': 'Please correct the errors below.',
                    'errors': errors
                }, status=400)

            # ------------------------------------------
            # Send Email via services.py file
            # ------------------------------------------
            email_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'subject': subject,
                'message': message
            }

            email_sent = send_contact_email(email_data)

            if not email_sent:
                logger.error("Contact email failed to send through services.py")
                return JsonResponse({
                    'success': False,
                    'message': 'Could not send your message right now. Please call us directly.'
                }, status=500)

            logger.info(f"Contact email successfully sent from {email}")

            # ------------------------------------------
            # Return success response
            # ------------------------------------------
            return JsonResponse({
                'success': True,
                'message': 'Thank you! Your message has been sent successfully. We will contact you within 24 hours.',
                'email_sent': email_sent
            }, status=200)

        except Exception as e:
            logger.error(f"Contact form error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'An unexpected error occurred. Please try again later.'
            }, status=500)

    # ------------------------------------------
    # GET request – render page
    # ------------------------------------------
    return render(request, 'contact.html')