from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Cart, CartItem


def _get_cart(request):
    """Return the current cart — user cart if logged in, session cart otherwise."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(
            session_key=request.session.session_key
        )
    return cart


def cart_detail(request):
    cart = _get_cart(request)
    return render(request, 'cart.html', {'cart': cart})


@require_POST
def add_to_cart(request):
    """Add a product to the cart."""
    name = request.POST.get('name', '').strip()
    price = request.POST.get('price', '0').strip()
    quantity = int(request.POST.get('quantity', 1))
    image = request.POST.get('image', '')

    if not name or not price:
        return JsonResponse(
            {'success': False, 'message': 'Product details missing.'},
            status=400
        )

    cart = _get_cart(request)
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product_name=name,
        defaults={
            'product_price': price,
            'quantity': quantity,
            'image_url': image,
        }
    )
    if not created:
        item.quantity += quantity
        item.save()

    return JsonResponse({
        'success': True,
        'cart_total_items': cart.get_total_items(),
    })


@require_POST
def update_cart_item(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (TypeError, ValueError):
        quantity = 1

    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()

    return JsonResponse({
        'success': True,
        'cart_total_items': cart.get_total_items(),
    })


@require_POST
def remove_cart_item(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return JsonResponse({
        'success': True,
        'cart_total_items': cart.get_total_items(),
    })


def cart_dropdown_api(request):
    cart = _get_cart(request)
    items = [
        {
            'name': i.product_name,
            'qty': i.quantity,
            'total': float(i.get_total_price()),
        }
        for i in cart.items.all()
    ]
    return JsonResponse({
        'items': items,
        'total_items': cart.get_total_items(),
    })