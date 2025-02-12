from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Order, OrderItem, Item, Category


@login_required(login_url='/home/')
def order(request):
    """
    Displays the ordering page.

    ***Context***
    ``user``
        The current user.
    ``items``
        All items in the database.
    ``categories``
        All categories in the database.
    """
    user = request.user
    items = Item.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        'ordering/order.html',
        {
            "user": user,
            "items": items,
            "categories": categories
        }
    )


@login_required
def order_view(request):
    """
    Displays the sent orders page.

    ***Context***
    ``user``
        The current user.
    ``orders``
        All orders made by the current user
    """
    user = request.user
    orders = Order.objects.filter(user=user).order_by("-created_at")
    return render(
        request,
        "ordering/order_list.html",
        {"orders": orders}
        )


@login_required
def order_items(request, order_id):
    """
    Retrieves the items in an order to display them.

    ***Context***
    ``order_items``
        The items in the order.
    ``status``
        The status of the order.
    """
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
    """
    Retrieves the items in the session to display them.

    ***Context***
    ``order_items``
        The items in the order.
    """
    order_items = request.session.get("order_items", [])
    return JsonResponse(
        {
            "success": "Order items retrieved successfully.",
            "order_items": order_items
        }
    )


def check_quantity_validity(quantity, item):
    """
    Checks if the quantity is valid by checking if it's a positive
    number and less than or equal to the quantity in stock.
    """
    if not isinstance(quantity, int) or quantity <= 0:
        return JsonResponse(
            {
                "error": "Invalid item or quantity.",
                "message": "The quantity must be a positive number."
            }, status=400)
    elif quantity > item.quantity_in_stock:
        return JsonResponse(
            {
                "error": "Insufficient stock.",
                "message": f"""Only {item.quantity_in_stock} {item.name} 
available."""
            }, status=400)
    else:
        return None


@login_required
def add_item_to_session(request):
    """
    Adds an item to the session.

    ***Context***
    ``item_id``
        The ID of the item to add.
    ``quantity``
        The quantity of the item to add.
    ``item``
        The item to add.
    ``order_items``
        The items in the order.
    """
    if request.method == "POST":
        item_id = request.POST.get("item")
        quantity_str = request.POST.get("item-quantity")
        item = get_object_or_404(Item, id=item_id)

        if not quantity_str.isdigit():
            return JsonResponse(
                {
                    "error": "Invalid item or quantity.",
                    "message": "The quantity must be a positive integer."
                }, status=400)

        quantity = int(quantity_str)

        if check_quantity_validity(quantity, item):
            return check_quantity_validity(quantity, item)

        order_items = request.session.get("order_items", [])
        # Check if the item is already in the order
        # If it is, update the quantity
        for item_in_order in order_items:
            if str(item_in_order["item_id"]) == item_id:
                new_quantity = item_in_order["quantity"] + quantity
                if new_quantity > item.quantity_in_stock:
                    return JsonResponse(
                        {
                            "error": "Insufficient stock.",
                            "message": f"""Only
{item.quantity_in_stock - item_in_order["quantity"]} {item.name} available."""
                        },
                        status=400
                    )
                item_in_order["quantity"] += quantity
                break
        else:
            order_items.append(
                {
                    "item_id": item_id,
                    "name": item.name,
                    "quantity": quantity
                })

        request.session["order_items"] = order_items
        return JsonResponse(
            {
                "success": "Item added to order.",
                "order_items": order_items
            })
    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required
def create_order(request):
    """
    Creates an order from the items in the session.

    ***Context***
    ``order_items``
        The items in the order.
    ``order``
        The order created.
    """
    if request.method == "POST":
        order_items = request.session.get("order_items", [])
        # Check if there are items to order
        if not order_items:
            return JsonResponse({"error": "No items to order."}, status=400)

        order_id = request.POST.get("order_id")
        try:
            if order_id:
                # Edit the order
                order = Order.objects.get(id=order_id, user=request.user)
                order.items.all().delete()
            else:
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

            return JsonResponse({"success": "Order saved successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@login_required
def delete_item(request, item_id):
    """
    Deletes an item from the session by filtering it out.

    ***Context***
    ``order_items``
        The items in the order.
    ``item_id``
        The ID of the item to delete.
    """
    if request.method == "POST":
        order_items = request.session.get("order_items", [])

        order_items = (
            [item for item in order_items if str(item["item_id"]) != item_id]
        )

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
    """
    Update the quantity of an item in the session.

    ***Context***
    ``quantity``
        The new quantity of the item.
    ``quantity_in_stock``
        The quantity of the item in stock.
    ``order_items``
        The items in the order
    """
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        quantity_in_stock = Item.objects.get(id=item_id).quantity_in_stock
        order_items = request.session.get("order_items", [])

        if int(quantity) > int(quantity_in_stock):
            return JsonResponse(
                {
                    "error": "Insufficient stock.",
                    "message": f"Only {quantity_in_stock} items available.",
                    "max_quantity": quantity_in_stock
                }, status=400)

        for item in order_items:
            if str(item["item_id"]) == item_id:
                item["quantity"] = int(quantity)
                break

        request.session["order_items"] = order_items
        return JsonResponse(
            {
                "success": "Item quantity updated.",
                "order_items": order_items
            })
    return JsonResponse({"error": "Invalid request method."}, status=405)


@login_required
def edit_order(request, order_id):
    """
    Edits an order by deleting the original order and creating a new one.

    ***Context***
    ``order``
        The order to edit.
    ``order_items``
        The items in the order.
    """
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order_items_db = order.items.all()

        order_items = []
        for item in order_items_db:
            order_items.append(
                {
                    "item_id": item.item.id,
                    "name": item.item.name,
                    "quantity": item.quantity
                })

        request.session["order_items"] = order_items

        return JsonResponse({"success": "Order edited successfully."})
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)


@login_required
def delete_order(request, order_id):
    """
    Deletes an order.

    ***Context***
    ``order``
        The order to delete.
    """
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        order.delete()
        return JsonResponse({"success": "Order deleted successfully."})
    except Order.DoesNotExist:
        return JsonResponse({"error": "Order not found."}, status=404)


def filter_items(request, category):
    """
    Filters items by category.

    ***Context***
    ``items``
        The items in the category.
    ``items_data``
        Prepare the items for JSON response.
    """

    items = Item.objects.filter(category__id=category)
    items_data = [{"id": item.id, "name": item.name} for item in items]

    return JsonResponse({"items": items_data})
