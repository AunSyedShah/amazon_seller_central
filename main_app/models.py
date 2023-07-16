from django.db import models
from django.contrib.auth.models import User
import uuid


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity_available = models.IntegerField(default=0)
    image = models.ImageField(upload_to="product_images", default='None', blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.price}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}'s Profile"


# Order and Order Model class

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    products = models.ManyToManyField(Product)
    total_price = models.IntegerField(default=0)
    order_status = models.CharField(max_length=100, default="Order Placed")
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Order id: {self.id} - User: {self.user.first_name} {self.user.last_name} - Total Price: {self.total_price} - Order Status: {self.order_status}"

    def get_order_items(self):
        return self.products.all()

    def get_order_total_price(self):
        return self.total_price

    def get_order_status(self):
        return self.order_status


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"Order id: {self.order.id} - Product: {self.product.name} - Quantity: {self.quantity} - Price: {self.price}"
