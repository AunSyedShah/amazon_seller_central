from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, default='profile_pics/default.png')
    default_shipping_address = models.CharField(max_length=100, blank=True, default='')
    default_billing_address = models.CharField(max_length=100, blank=True, default='')
    date_of_birth = models.DateField(blank=True, null=True, default=None)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.user.username
