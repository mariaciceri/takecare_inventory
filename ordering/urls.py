from . import views
from django.urls import path

urlpatterns = [
    path("", views.order, name="order"),
    path(
        "add_item_to_session/",
        views.add_item_to_session,
        name="add_item_to_session"
    ),
    path("create_order/", views.create_order, name="create_order"),
    path("edit_order/<str:order_id>", views.edit_order, name="edit_order"),
    path(
        "delete_order/<str:order_id>", views.delete_order, name="delete_order"
    ),
    path("delete_item/<str:item_id>", views.delete_item, name="delete_item"),
    path(
        "filter_items/<str:category>", views.filter_items, name="filter_items"
    ),
    path("orders/", views.order_view, name="order_view"),
    path("orders/order<str:order_id>", views.order_items, name="order_items"),
    path("session_items/", views.session_items, name="session_items"),
    path(
        "update_item_quantity/<str:item_id>",
        views.update_item_quantity,
        name="update_item_quantity"
    ),
]
