from django.db import models
from django.contrib.auth.models import User
import uuid


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity_available = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.price}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}'s Profile"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
