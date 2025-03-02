# admin.py
from django.contrib import admin
from .models import Prize, SpinResult

admin.site.register(Prize)
admin.site.register(SpinResult)