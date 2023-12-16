from django.shortcuts import render


def index(request):
    return render(request, 'dashboard.html')

def profile(request):
    return render(request, 'profile.html')

def inbox(request):
    return render(request, 'tables.html')

def send_task(request):
    return render(request, 'tables.html')

