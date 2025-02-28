from django.shortcuts import render


def index(request):
    return render(request, "OneLastMerch/index.html", context={"user": request.user})
