from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    name = models.CharField(max_length=255,unique=True)
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(blank=True, default='defaults/default_product.jpg', upload_to='product_pics')
    desc = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)
    # stock = models.PositiveIntegerField(default=0)
    cart_max = models.PositiveIntegerField(default=8)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def isOnSale(self):
        if self.sale_price is not None:
            if self.sale_price < self.price:
                return True
        return False
    
    #should use this now
    def actualPrice(self):
        if self.sale_price is not None:
            if self.sale_price < self.price:
                return self.sale_price
        return self.price
    
    def descShort(self):
        if len(self.desc)>25:
            return self.desc[:25]+'...'
        return self.desc
    
    # def isAvailable(self):
    #     if self.stock > 0:
    #         return True
    #     return False


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)

    def item_qty_price(self):
        # return self.prod.actualPrice() * self.qty
        if(self.prod.isOnSale()):
            return self.prod.sale_price * self.qty
        return self.prod.price * self.qty
    
    def __str__(self):
        return f"{self.prod} - {self.user}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # required now
    uemail = models.EmailField(max_length=20, null=True)
    phone = models.CharField(max_length=20)
    street = models.CharField(max_length=150)
    address = models.TextField()
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=12)

    delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order for {self.user} - {self.created_at}"

    def ord_total_price(self):
        # return sum(orderItem.total_price() for orderItem in self.orderitems.all())
        total = 0.0
        for orderItem in self.orderitem_set.all():
            total += float(orderItem.total_price())
        return round(total,2)
    
    def total_qty(self):
        total = 0
        for orderItem in self.orderitem_set.all():
            total += orderItem.qty
        return total
    
    def total_products(self):
        return self.orderitem_set.all().count()
    
    def delivery_add(self):
        return f"{self.street}, {self.address}, {self.city}, {self.country} - {self.zipcode}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE) # related_name='orderitems'
    prod = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 


    def __str__(self):
        return f"{self.order.user} - {self.prod} - {self.qty}"

    def total_price(self):
        return self.price * self.qty
