from django.urls import path
from .views import LogInView, RegisterView


urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name = 'register'),

]
