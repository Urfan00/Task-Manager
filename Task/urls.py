from django.urls import path
from .views import TaskCreateView, inbox, send_task



urlpatterns = [
    path('send_task/', send_task, name='send_task'),
    path('inbox/', inbox, name='inbox'),

    path('create/', TaskCreateView.as_view(), name='create'),
]
