from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    #image = models.ImageField(upload_to='products/', blank=True, null=True)
    #created_at = models.DateTimeField(auto_now_add=True)
    #updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username

class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    shipping_address = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.pk}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
    def calculate_total_price(self):
        total = 0.0
        for order_item in self.items.all():
            total += order_item.product.price * order_item.quantity
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order Item #{self.pk} - Product: {self.product.name}, Quantity: {self.quantity}"
    
    
    