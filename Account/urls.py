from django.urls import path
from .views import ChangePasswordView, LogInView, RegisterView, ResetPasswordConfirmView, ResetPasswordView, logout_view


urlpatterns = [
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
    path('reset_password_confirm/<str:uidb64>/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
]
