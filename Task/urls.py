from django.urls import path
from .views import inbox, send_task



urlpatterns = [
    path('inbox/', inbox, name='inbox'),
    path('send_task/', send_task, name='send_task'),
]
