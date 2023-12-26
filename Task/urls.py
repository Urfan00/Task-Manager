from django.urls import path
from .views import AssignedTaskListView, BinListView, ForwardFormView, ForwardTaskListView, InboxListView, SendTaskListView, TaskCreateView, TaskDetailView, toggle_action_status, toggle_action_status_forward



urlpatterns = [
    path('inbox/', InboxListView.as_view(), name='inbox'),
    path('send_task/', SendTaskListView.as_view(), name='send_task'),
    path('create/', TaskCreateView.as_view(), name='create'),
    path('bin/', BinListView.as_view(), name='bin'),
    path('task_detail/<int:pk>', TaskDetailView.as_view(), name='task_detail'),

    path('forwarded/', ForwardTaskListView.as_view(), name='forwarded'),
    path('assigned/', AssignedTaskListView.as_view(), name='assigned'),
    path('task_forward/<int:pk>', ForwardFormView.as_view(), name='task_forward'),


    path('toggle_action_status/', toggle_action_status, name='toggle_action_status'),
    path('toggle_action_status_forward/', toggle_action_status_forward, name='toggle_action_status_forward'),

]
