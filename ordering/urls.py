from . import views
from django.urls import path

urlpatterns = [
    path('', views.order, name='order'),
    path('orders/', views.order_view, name='order_view'),
]