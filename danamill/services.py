# services.py
import logging
from django.core.mail import EmailMessage
from django.conf import settings

logger = logging.getLogger(__name__)

def send_contact_email(data):
    """
    Handles sending the contact email via SMTP.
    Returns True if successful, False otherwise.
    """
    try:
        email_subject = f"[Website Enquiry] {data.get('subject', 'New Message')}"
        
        email_body = f"""
========================================
NEW CONTACT FORM SUBMISSION
========================================

👤 Name    : {data.get('name')}
📧 Email   : {data.get('email')}
📞 Phone   : {data.get('phone')}
📝 Subject : {data.get('subject')}

----------------------------------------
Message:
----------------------------------------
{data.get('message')}

========================================
This message was sent from the Jai Durga Plastic website.
========================================
        """.strip()

        email_message = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_RECEIVER_EMAIL],
            reply_to=[data.get('email')],
        )
        
        email_message.send(fail_silently=False)
        logger.info(f"Contact email successfully sent from {data.get('email')}")
        return True

    except Exception as mail_error:
        logger.error(f"Contact email failed via SMTP: {str(mail_error)}")
        return False