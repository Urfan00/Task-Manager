from django.urls import path
from .views import inbox, index, profile, send_task


urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('inbox/', inbox, name='inbox'),
    path('send_task/', send_task, name='send_task'),
]
