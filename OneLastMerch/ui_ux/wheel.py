from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random

# Define prizes and their probabilities
PRIZES = [
    {"text": "10% Off", "code": "DISCOUNT10", "chance": 30},
    {"text": "Free Shipping", "code": "FREESHIP", "chance": 20},
    {"text": "5% Off", "code": "DISCOUNT5", "chance": 25},
    {"text": "Mystery Gift", "code": "MYSTERY", "chance": 15},
    {"text": "Try Again", "code": None, "chance": 5},
    {"text": "20% Off", "code": "DISCOUNT20", "chance": 5},
]

def weighted_choice(prizes):
    """Select a prize based on weighted probabilities."""
    choices = []
    for prize in prizes:
        choices.extend([prize] * prize["chance"])
    return random.choice(choices)

@login_required
def spin_wheel(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Return a random prize for AJAX requests
        winning_prize = weighted_choice(PRIZES)
        return JsonResponse({"reward": winning_prize, "total_prizes": len(PRIZES)})
    
    # Render the wheel template for regular requests
    return render(request, "ui_ux/wheel.html", {"prizes": PRIZES})