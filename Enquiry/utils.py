import logging
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import EnquiryLog

logger = logging.getLogger(__name__)

def send_enquiry_notifications(enquiry):
    """
    Send email notifications for a new enquiry:
    1. Admin notification email
    2. Customer acknowledgment email
    """
    
    results = {
        'admin_sent': False,
        'customer_sent': False,
        'errors': []
    }
    
    # 1. Send Admin Notification
    admin_sent = send_admin_notification(enquiry)
    results['admin_sent'] = admin_sent
    
    # 2. Send Customer Acknowledgment
    customer_sent = send_customer_acknowledgment(enquiry)
    results['customer_sent'] = customer_sent
    
    return results

def send_admin_notification(enquiry):
    """Send email notification to admin about new enquiry"""
    try:
        subject = f"New Enquiry: {enquiry.name} - {enquiry.product}"
        
        # HTML Email Template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #1a4a8a; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background: #f8f9fa; }}
                .detail-row {{ margin: 15px 0; padding: 10px; background: white; border-radius: 5px; }}
                .label {{ font-weight: bold; color: #1a4a8a; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>New Enquiry Received</h2>
                    <p>DanaMill - Customer Enquiry System</p>
                </div>
                <div class="content">
                    <div class="detail-row">
                        <div class="label">Customer Name:</div>
                        <div>{enquiry.name}</div>
                    </div>
                    <div class="detail-row">
                        <div class="label">Email:</div>
                        <div>{enquiry.email}</div>
                    </div>
                    <div class="detail-row">
                        <div class="label">Phone:</div>
                        <div>{enquiry.phone}</div>
                    </div>
                    <div class="detail-row">
                        <div class="label">Product:</div>
                        <div>{enquiry.product}</div>
                    </div>
                    <div class="detail-row">
                        <div class="label">Message/Quantity:</div>
                        <div>{enquiry.message}</div>
                    </div>
                    <div class="detail-row">
                        <div class="label">Enquiry Date:</div>
                        <div>{enquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')}</div>
                    </div>
                </div>
                <div class="footer">
                    <p>You can view all enquiries in the admin panel.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMIN_EMAIL],
            reply_to=[enquiry.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        # Log the email
        EnquiryLog.objects.create(
            enquiry=enquiry,
            email_type='admin_notification',
            sent_to=settings.ADMIN_EMAIL,
            status='success'
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send admin notification: {str(e)}")
        EnquiryLog.objects.create(
            enquiry=enquiry,
            email_type='admin_notification',
            sent_to=settings.ADMIN_EMAIL,
            status='failed',
            error_message=str(e)
        )
        return False

def send_customer_acknowledgment(enquiry):
    """Send acknowledgment email to customer"""
    try:
        subject = f"Thank you for your enquiry - DanaMill"
        
        # HTML Email Template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1a4a8a, #2c6e9e); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; background: #f8f9fa; }}
                .thank-you {{ font-size: 24px; margin-bottom: 20px; }}
                .details {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .cta-button {{ display: inline-block; padding: 12px 30px; background: #1a4a8a; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>DanaMill</h1>
                    <p>Premium Plastic Granules Manufacturer</p>
                </div>
                <div class="content">
                    <div class="thank-you">Thank You, {enquiry.name}! 👋</div>
                    <p>We have received your enquiry for <strong>{enquiry.product}</strong>.</p>
                    
                    <div class="details">
                        <h3>Your Enquiry Details:</h3>
                        <p><strong>Product:</strong> {enquiry.product}</p>
                        <p><strong>Message:</strong> {enquiry.message}</p>
                        <p><strong>Enquiry ID:</strong> #{enquiry.id}</p>
                        <p><strong>Date:</strong> {enquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                    </div>
                    
                    <p>Our team will contact you within <strong>24 hours</strong> to discuss your requirements.</p>
                    
                    <div style="text-align: center;">
                        <a href="#" class="cta-button">Visit Our Website</a>
                    </div>
                </div>
                <div class="footer">
                    <p>© 2024 DanaMill. All rights reserved.</p>
                    <p>123 Industrial Area, Mumbai - 400001</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = strip_tags(html_content)
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[enquiry.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        
        # Log the email
        EnquiryLog.objects.create(
            enquiry=enquiry,
            email_type='customer_acknowledgment',
            sent_to=enquiry.email,
            status='success'
        )
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to send customer acknowledgment: {str(e)}")
        EnquiryLog.objects.create(
            enquiry=enquiry,
            email_type='customer_acknowledgment',
            sent_to=enquiry.email,
            status='failed',
            error_message=str(e)
        )
        return False

def send_enquiry_emails(enquiry):
    """
    Alternative function name for backward compatibility
    Calls the main send_enquiry_notifications function
    """
    return send_enquiry_notifications(enquiry)