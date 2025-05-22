from django.contrib import admin
from merchstore.models import Category, Product, CartItem, OrderItem, Order

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(OrderItem)
admin.site.register(Order)
