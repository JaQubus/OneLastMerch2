from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random
from .models import Prize, SpinResult

# Render the wheel UI
def spin_wheel_ui(request):
    prizes = Prize.objects.all()
    segment_angle = 360 / len(prizes) if prizes else 0  # Calculate segment angle
    return render(request, 'ui_ux/wheel.html', {'prizes': prizes, 'segment_angle': segment_angle})

# Handle the spin logic and save the result
@login_required
def spin_wheel_api(request):
    if SpinResult.objects.filter(user=request.user).exists():
        return JsonResponse({'error': 'You have already spun the wheel.'}, status=400)

    prizes = Prize.objects.all()
    prize_list = list(prizes)
    probabilities = [prize.probability for prize in prize_list]

    # Randomly select a prize based on probability
    selected_prize = random.choices(prize_list, weights=probabilities, k=1)[0]

    # Save the result to the database
    SpinResult.objects.create(user=request.user, prize=selected_prize)

    # Return the result to the frontend
    return JsonResponse({'prize_name': selected_prize.name, 'prize_index': prize_list.index(selected_prize)})