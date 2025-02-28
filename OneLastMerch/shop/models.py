from django.db import models
from django.core.validators import MinLengthValidator

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
