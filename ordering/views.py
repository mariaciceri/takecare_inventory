from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import JsonResponse
from .models import Order, CustomUser, OrderItem, Item
from .forms import OrderForm, OrderItemForm, OrderItemInlineForm

OrderItemFormSet = modelformset_factory(
    OrderItem, form=OrderItemInlineForm
)

@login_required
def order(request):
    user = request.user

    return render(
        request,
        'ordering/order.html',
        {'user': user}
        )

@login_required
def order_view(request):
    user = request.user
    orders = Order.objects.filter(user=user)

    return render(
        request,
        'ordering/order_list.html',
        {'orders': orders}
        )

@login_required
def create_order(request):
    if request.method == 'POST':
        order = Order(user=request.user)
        order.save()

        # Get the order items stored in the session
        order_items_data = request.session.get('order_items', [])

        if not order_items_data:
            # If no items are selected, show an error
            return JsonResponse({"error": "No items selected."})

        # Loop through the stored items and create OrderItems
        for item_data in order_items_data:
            item = Item.objects.get(id=item_data['item_id'])
            quantity = item_data['quantity']

            # Create OrderItem and associate with the created order
            order_item = OrderItem(order=order, item=item, quantity=quantity)
            order_item.save()

        # Clear the session data
        request.session['order_items'] = []

        return redirect('order_list.html')
    else:
        # Display the order form (initial load or if GET request)
        return render(request, 'create_order.html')
