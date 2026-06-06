from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Cart, CartItem

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_detail(request):
    cart = get_cart(request)
    context = {'cart': cart}
    return render(request, 'cart/cart.html', context)

@require_http_methods(["POST"])
def add_to_cart(request):
    product_name = request.POST.get('name')
    product_price = request.POST.get('price')
    quantity = int(request.POST.get('quantity', 1))
    image_url = request.POST.get('image', '')

    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_name=product_name,
        defaults={'product_price': product_price, 'quantity': quantity, 'image_url': image_url}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return JsonResponse({'success': True, 'cart_total_items': cart.get_total_items()})

@require_http_methods(["POST"])
def update_cart_item(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    return JsonResponse({'success': True, 'cart_total_items': cart.get_total_items()})

@require_http_methods(["POST"])
def remove_cart_item(request, item_id):
    cart = get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return JsonResponse({'success': True, 'cart_total_items': cart.get_total_items()})


def cart_dropdown_api(request):
    cart = get_cart(request)
    items = [{'name': i.product_name, 'qty': i.quantity, 'total': float(i.get_total_price())} for i in cart.items.all()]
    return JsonResponse({'items': items, 'total_items': cart.get_total_items()})