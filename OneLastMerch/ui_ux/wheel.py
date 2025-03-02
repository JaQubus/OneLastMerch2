import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Prize, SpinResult

@login_required
def spin_wheel(request):
    # Prevent user from spinning more than once
    if SpinResult.objects.filter(user=request.user).exists():
        messages.error(request, "You can only spin once!")
        return redirect('spin_result')

    prizes = list(Prize.objects.all())
    total_prizes = len(prizes)
    if total_prizes == 0:
        messages.error(request, "No prizes available!")
        return render(request, 'ui_ux/wheel.html')

    angle_per_prize = 360 / total_prizes
    for index, prize in enumerate(prizes):
        prize.angle = index * angle_per_prize
        prize.mid_angle = prize.angle + (angle_per_prize / 2)  # Midpoint of segment

    return render(request, 'ui_ux/wheel.html', {'prizes': prizes})

@login_required
def spin_wheel_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

    # Prevent multiple spins
    if SpinResult.objects.filter(user=request.user).exists():
        return JsonResponse({'error': 'You can only spin once!'}, status=400)

    prizes = list(Prize.objects.all())
    total_prizes = len(prizes)
    if total_prizes == 0:
        return JsonResponse({'error': 'No prizes available.'}, status=400)

    angle_per_prize = 360 / total_prizes
    for index, prize in enumerate(prizes):
        prize.angle = index * angle_per_prize

    # Select a prize based on weighted probabilities
    probabilities = [prize.probability for prize in prizes]
    selected_prize = random.choices(prizes, weights=probabilities, k=1)[0]
    prize_index = prizes.index(selected_prize)

    # Save the spin result
    SpinResult.objects.create(user=request.user, prize=selected_prize)

    return JsonResponse({
        'prize_index': prize_index,
        'prize_name': selected_prize.name,
    })

@login_required
def spin_result(request):
    try:
        result = SpinResult.objects.get(user=request.user)
    except SpinResult.DoesNotExist:
        return redirect('spin_wheel')

    return render(request, 'ui_ux/spin_result.html', {'result': result})
