from django.urls import path
from .views import InboxListView, SendTaskListView, TaskCreateView



urlpatterns = [
    path('inbox/', InboxListView.as_view(), name='inbox'),
    path('send_task/', SendTaskListView.as_view(), name='send_task'),
    path('create/', TaskCreateView.as_view(), name='create'),
]
