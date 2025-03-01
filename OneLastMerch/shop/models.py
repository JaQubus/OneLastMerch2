from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

class Item(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    image = models.ImageField(null=False)
    title = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(3)],
        null=True,
        unique=True
    )
    tag = models.CharField(
        max_length=15,
        validators=[MinLengthValidator(3)],
        null=True
    )
    price = models.FloatField(null=True)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=50, blank=True, null=True, unique=True)

    def __str__(self):
        return f"Cart ({self.user if self.user else 'Guest'})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey("shop.Item", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.item.title} in Cart {self.cart}"
