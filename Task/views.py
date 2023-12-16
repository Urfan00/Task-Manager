from django.shortcuts import render

# Create your views here.

def inbox(request):
    return render(request, 'tables.html')

def send_task(request):
    return render(request, 'tables.html')