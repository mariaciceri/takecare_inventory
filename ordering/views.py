from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.forms import modelformset_factory
from django.http import JsonResponse
from .models import Order, OrderItem, Item
from .forms import OrderItemInlineForm

OrderItemFormSet = modelformset_factory(
    OrderItem, form=OrderItemInlineForm
)

@login_required
def order(request):
    user = request.user
    items = Item.objects.all()

    return render(
        request,
        'ordering/order.html',
            {
            "user": user,
            "items": items
            }
        )

@login_required
def order_view(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by("-created_at")

    return render(
        request,
        'ordering/order_list.html',
        {'orders': orders}
        )

@login_required
def order_items(request, order_id):
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items = order.items.all()

        order_items_list = [
            {
                "name": item.item.name,
                "quantity": item.quantity,
            }
            for item in order_items
        ]

        return JsonResponse(
            {
                "order_items": order_items_list,
                "status": order.status
            })
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)

@login_required
def session_items(request):
    try:
        order_items = request.session.get("order_items", [])
        return JsonResponse(
            {
                "success": "Order items retrieved successfully.",
                "order_items": order_items
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@login_required
def add_item_to_session(request):
    if request.method == "POST":
        item_id = request.POST.get("item")
        quantity = request.POST.get("item-quantity")

        if not quantity or not quantity.isdigit() or int(quantity) <= 0:
            return JsonResponse(
                {
                    "error": "Invalid item or quantity.",
                    "message": "The quantity must be a positive number."
                },
                status=400
            )

        quantity = int(quantity)
        
        item = get_object_or_404(Item, id=item_id)

        if quantity > item.quantity_in_stock:
                return JsonResponse(
                {
                    "error": "Insufficient stock.",
                    "message": f"Only {item.quantity_in_stock} {item.name} available."
                },
                status=400
            )
            
        order_items = request.session.get("order_items", [])

        for item_in_order in order_items:
            if item_in_order["item_id"] == item_id:
                if item_in_order["quantity"] + quantity > item.quantity_in_stock:
                    return JsonResponse(
                        {
                            "error": "Insufficient stock.",
                            "message": f"Only {item.quantity_in_stock} {item.name} available."
                        },
                        status=400
                    )
                item_in_order["quantity"] += quantity
                break
        else:
            order_items.append({"item_id": item_id, "name": item.name ,"quantity": quantity})

        request.session["order_items"] = order_items

        return JsonResponse(
            {
                "success": "Item added to order.",
                "order_items": order_items
            }
            )
    return JsonResponse({"error": "Invalid request method."}, status=405)

@login_required
def create_order(request):
    if request.method == "POST":
        order_items = request.session.get("order_items", [])
        if not order_items:
            return JsonResponse({"error": "No items to order."}, status=400)
        
        try:

            # Create the order
            order = Order(user=request.user)
            order.save()

            # Create the order items
            for item_data in order_items:
                item = Item.objects.get(id=item_data['item_id'])
                quantity = item_data['quantity']

                order_item = OrderItem(
                    order=order,
                    item=item,
                    quantity=quantity
                    )
                order_item.save()

            # Clear the session
            del request.session["order_items"]

            return JsonResponse({"success": "Order created successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)

@login_required
def delete_item(request, item_id):
    if request.method == "POST":
        order_items = request.session.get("order_items", [])

        order_items = [item for item in order_items if item["item_id"] != item_id]

        request.session["order_items"] = order_items
        return JsonResponse(
            {
                "success": "Item removed from order.",
                "order_items": order_items
            }
        )
    return JsonResponse({"error": "Invalid request method."}, status=405)

@login_required
def update_item_quantity(request, item_id):
    if request.method == "POST":
        quantity = request.POST.get("quantity")

        order_items = request.session.get("order_items", [])

        if not quantity or not quantity.isdigit() or int(quantity) <= 0:
            return JsonResponse(
                {
                    "error": "Invalid item or quantity.",
                    "message": "The quantity must be a positive number."
                },
                status=400
            )
        
        for item in order_items:
            if item["item_id"] == item_id:
                item["quantity"] = int(quantity)
                break

        request.session["order_items"] = order_items
        return JsonResponse(
            {
                "success": "Item quantity updated.",
                "order_items": order_items
            }
        )
    return JsonResponse({"error": "Invalid request method."}, status=405)

@login_required
def edit_order(request, order_id):
    pass
