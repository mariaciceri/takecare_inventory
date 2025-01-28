from . import views
from django.urls import path

urlpatterns = [
    path("", views.order, name="order"),
    path("add_item_to_session/", views.add_item_to_session, name="add_item_to_session"),
    path("create_order/", views.create_order, name="create_order"),
    path("session_items/", views.session_items, name="session_items"),
    path("orders/", views.order_view, name="order_view"),
]