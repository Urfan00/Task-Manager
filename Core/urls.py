from django.urls import path
from .views import ProfileView, index


urlpatterns = [
    path('', index, name='index'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
