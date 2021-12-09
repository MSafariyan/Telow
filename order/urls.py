from django.contrib import admin
from django.urls import path, include
from .views import OrderListView, OrderCreat, OrderDetail, OrderMetaUpdate, order_search

urlpatterns = [
    path('', OrderListView, name="order-list"),
    path('create', OrderCreat, name="order-creat"),
    path('<pk>', OrderDetail, name="order-detail"),
    path('order-meta/<pk>', OrderMetaUpdate.as_view(), name="order-meta-status"),
    path('search/order', order_search, name="order-search")
]