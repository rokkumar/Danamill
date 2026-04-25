from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
import logging

from .forms import QuickEnquiryForm
from .models import Enquiry, EnquiryLog
from .utils import send_enquiry_notifications  

# Initialize logger
logger = logging.getLogger(__name__)

def home(request):
    """Home page view"""
    context = {
        'page_title': 'DanaMill - Premium Plastic Granules Manufacturer',
        'current_year': 2024,
    }
    return render(request, 'home.html', context)

@require_http_methods(["POST"])
def submit_quick_enquiry(request):
    """
    API endpoint to handle quick enquiry form submissions
    """
    try:
        # Handle both JSON and Form data
        if request.content_type and request.content_type.startswith('application/json'):
            # If JSON request
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid JSON format.'
                }, status=400)
        else:
            # If form data
            data = request.POST.dict()
        
        # Create form with data
        form = QuickEnquiryForm(data)
        
        if form.is_valid():
            # Save the enquiry to database
            enquiry = form.save()
            
            # Send email notifications
            try:
                email_results = send_enquiry_notifications(enquiry)
            except Exception as e:
                logger.error(f"Email error but enquiry saved: {str(e)}")
                email_results = {'admin_sent': False, 'customer_sent': False}
            
            # Prepare response
            response_data = {
                'success': True,
                'message': 'Enquiry submitted successfully! We will contact you soon.',
                'enquiry_id': enquiry.id,
                'emails_sent': {
                    'admin': email_results.get('admin_sent', False),
                    'customer': email_results.get('customer_sent', False)
                }
            }
            
            logger.info(f"New enquiry #{enquiry.id} from {enquiry.name}")
            
            return JsonResponse(response_data, status=200)
        else:
            # Form validation errors
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            
            logger.warning(f"Form validation errors: {errors}")
            
            return JsonResponse({
                'success': False,
                'message': 'Please correct the errors below.',
                'errors': errors
            }, status=400)
            
    except Exception as e:
        logger.error(f"Error processing enquiry: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred. Please try again later.'
        }, status=500)

@require_http_methods(["GET"])
def get_enquiry_status(request, enquiry_id):
    """
    Get status of a specific enquiry (optional - for future use)
    """
    try:
        enquiry = Enquiry.objects.get(id=enquiry_id)
        return JsonResponse({
            'success': True,
            'enquiry_id': enquiry.id,
            'status': enquiry.get_status_display(),
            'created_at': enquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Enquiry.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Enquiry not found.'
        }, status=404)
