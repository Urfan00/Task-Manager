from django.urls import path
from .views import BinListView, InboxListView, SendTaskListView, TaskCreateView, toggle_action_status



urlpatterns = [
    path('inbox/', InboxListView.as_view(), name='inbox'),
    path('send_task/', SendTaskListView.as_view(), name='send_task'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('bin/', BinListView.as_view(), name='bin'),

    path('toggle_action_status/', toggle_action_status, name='toggle_action_status'),

]
