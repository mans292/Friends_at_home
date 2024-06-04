from django.db import models
from django.contrib.auth.models import User


class Products(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    kvantitet = models.IntegerField(default=0)

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shipped = models.BooleanField(default=False)
    item = models.ManyToManyField(Products, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField()

   
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
  

class Cart(models.Model):
    
    session_id = models.CharField(max_length=50, unique=True, null=True)
    items = models.ManyToManyField(Products, through='CartItem')
    
    def remove_from_cart(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
    
    def add_to_cart(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=self, product=product)
    
    def add_quantity(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=self, product=product)
    
    def decrease_quantity(self, product):
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.quantity -= 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart=self, product=product)        

  


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    
