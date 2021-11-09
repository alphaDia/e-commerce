from django.db import models
from store.models import Product, Variation
from uuid import uuid4


class Cart(models.Model):
    cart_id     = models.CharField(max_length=255, unique=True)
    date_added  = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.cart_id
    


class CartItem(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size    = models.CharField(max_length=100, default=0)
    product_color   = models.CharField(max_length=100, default="")
    cart            = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity        = models.IntegerField()
    is_active       = models.BooleanField(default=True)
    
    def sub_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return self.product.name