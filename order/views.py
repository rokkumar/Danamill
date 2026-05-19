from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import OrderForm

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            
            # Send email to customer
            subject = f"Order Confirmation - {order.product} Granules"
            message = f"""
            Dear {order.customer_name},

            Thank you for your order. Here are the details:
            Product: {order.product}
            Quantity: {order.quantity}
            Name: {order.customer_name}
            Email: {order.email}
            Phone: {order.phone}
            Address: {order.address}
            Message: {order.message}

            We will contact you shortly with a quote.

            Best regards,
            PlastiCorp Team
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [order.email]
            
            # ✅ Store customer name in session
            request.session['order_customer_name'] = order.customer_name
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            
            # Optional: send notification to admin
            admin_subject = f"New Order from {order.customer_name}"
            admin_message = f"Product: {order.product}\nQuantity: {order.quantity}\nCustomer: {order.customer_name}\nEmail: {order.email}\nPhone: {order.phone}\nAddress: {order.address}"
            send_mail(admin_subject, admin_message, from_email, [settings.ADMIN_EMAIL], fail_silently=True)
            
            messages.success(request, 'Your quote request has been sent! Check your email for confirmation.')
            return redirect('order:order_success')
    else:
        # Pre-fill product from GET parameter
        initial_product = request.GET.get('product', '')
        form = OrderForm(initial={'product': initial_product})
    
    return render(request, 'order/order_form.html', {'form': form})

def order_success(request):
    customer_name = request.session.pop('order_customer_name', None)
    return render(request, 'order/order_success.html',{'customer_name': customer_name})

