from django.urls import path
from .views import InboxView, ProfileView


urlpatterns = [
    path('', InboxView.as_view(), name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
