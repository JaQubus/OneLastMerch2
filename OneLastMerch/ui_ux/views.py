from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  # Ensure the user is logged in to access this view
def account(request):
    # Fetch the username and email for the logged-in user
    context = {
        "username": request.user.username,
        "email": request.user.email,
    }
    return render(request, 'ui_ux/account.html', context=context)  # Render the account page with user data

def about_us(request):
    return render(request, 'ui_ux/about-us.html')
