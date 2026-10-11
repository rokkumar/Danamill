from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import Event, EventItem
from .forms import EventForm, EventItemForm


staff_only = user_passes_test(
    lambda u: u.is_authenticated and u.is_staff,
    login_url='/login/',
)


# =====================================================================
# EVENT LIST
# =====================================================================

@login_required
@staff_only
def event_list(request):
    events = Event.objects.all().order_by('-start_date', '-id')
    return render(request, 'events/event_list.html', {'events': events})


# =====================================================================
# EVENT DETAIL (Excel-style statement)
# =====================================================================

@login_required
@staff_only
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    items = event.items.all().order_by('id')

    # Attach pending to each item (computed on the fly)
    items_with_pending = []
    for item in items:
        items_with_pending.append({
            'item': item,
            'pending': item.total_cost - item.paid_amount,
        })

    total_expenses = event.total_expenses()
    total_paid = event.total_paid()
    total_pending = event.total_pending()
    remaining_funds = event.remaining_funds()

    context = {
        'event': event,
        'items': items_with_pending,
        'total_expenses': total_expenses,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'remaining_funds': remaining_funds,
    }
    return render(request, 'events/event_detail.html', context)


# =====================================================================
# EVENT CREATE
# =====================================================================

@login_required
@staff_only
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Event '{event.name}' created.")
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form, 'is_edit': False})


# =====================================================================
# EVENT EDIT
# =====================================================================

@login_required
@staff_only
def event_edit(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated.")
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {
        'form': form, 'is_edit': True, 'event': event,
    })


# =====================================================================
# EVENT DELETE
# =====================================================================

@login_required
@staff_only
def event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted.")
        return redirect('events:event_list')
    return render(request, 'events/event_confirm_delete.html', {'event': event})


# =====================================================================
# ITEM ADD
# =====================================================================

@login_required
@staff_only
def item_create(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.event = event
            item.save()
            messages.success(request, f"Item '{item.item_name}' added.")
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventItemForm()
    return render(request, 'events/item_form.html', {
        'form': form, 'event': event, 'is_edit': False,
    })


# =====================================================================
# ITEM EDIT
# =====================================================================

@login_required
@staff_only
def item_edit(request, item_id):
    item = get_object_or_404(EventItem, id=item_id)
    event = item.event
    if request.method == 'POST':
        form = EventItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated.")
            return redirect('events:event_detail', event_id=event.id)
    else:
        form = EventItemForm(instance=item)
    return render(request, 'events/item_form.html', {
        'form': form, 'event': event, 'is_edit': True, 'item': item,
    })


# =====================================================================
# ITEM DELETE
# =====================================================================

@login_required
@staff_only
def item_delete(request, item_id):
    item = get_object_or_404(EventItem, id=item_id)
    event = item.event
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted.")
        return redirect('events:event_detail', event_id=event.id)
    return render(request, 'events/item_confirm_delete.html', {
        'item': item, 'event': event,
    })