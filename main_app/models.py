from PIL import Image
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    quantity_available = models.IntegerField(default=0)
    image = models.ImageField(upload_to="product_images", blank=True, null=True)
    order_quantity = models.IntegerField(default=0, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", blank=True,
                                 null=True)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.price}"

    # override save to resize image
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # resize image
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}'s Profile"


# Order and Order Model class

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name="products")
    total_price = models.IntegerField(default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    # approved, pending, delivered, cancelled
    order_status_choices = [
        ("Approved", "Approved"),
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    order_status = models.CharField(
        max_length=10, choices=order_status_choices, default="Pending"
    )

    def __str__(self) -> str:
        return f"Order id: {self.id} - User: {self.user.first_name} {self.user.last_name} - Total Price: {self.total_price} - Order Status: {self.order_status}"

    def get_order_items(self):
        return self.products.all()

    def get_order_total_price(self):
        return self.total_price

    def get_order_status(self):
        return self.order_status

    # get quantity of a product in an order
    def get_product_quantity(self, product):
        return self.products.filter(id=product.id).count()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="reviews")
    cnic = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} - {self.review} - {self.rating} - {self.date}"
