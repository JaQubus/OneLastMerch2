# models.py
from django.db import models
from django.contrib.auth.models import User

class Prize(models.Model):
    name = models.CharField(max_length=100)
    probability = models.FloatField(help_text="Probability of winning this prize (0-1)")

    def __str__(self):
        return self.name

class SpinResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    spin_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} won {self.prize.name} on {self.spin_date}"