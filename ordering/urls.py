from . import views
from django.urls import path

urlpatterns = [
    path("", views.order, name="order"),
    path("add_item_to_session/", views.add_item_to_session, name="add_item_to_session"),
    path("create_order/", views.create_order, name="create_order"),
    path("delete_item/<str:item_id>", views.delete_item, name="delete_item"),
    path("orders/", views.order_view, name="order_view"),
    path("session_items/", views.session_items, name="session_items"),
    path("update_item_quantity/<str:item_id>", views.update_item_quantity, name="update_item_quantity"),
]