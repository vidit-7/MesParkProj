from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.merchHome, name="merchStoreHome"),
    path('product/<str:pk>', views.merchProduct, name="merchStoreProduct"),
    path('cart/', views.merchCart, name="merchStoreCart"),
    path('update-cart/',views.merchUpdateCart, name="merchStoreUpdateCart"),
    path('checkout/', views.merchCheckout, name="merchStoreCheckout"),
    path('orders/',views.merchOrders, name="merchStoreOrders"),
]