from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm,
                                      UsernameField,
                                      UserCreationForm,
                                      PasswordResetForm,
                                      PasswordChangeForm,
                                      SetPasswordForm)


User = get_user_model()

# LOGIN FORM
class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder' : 'Email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder' : 'Password'
            }
        )
    )


# Registration FORM
class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'number', 'email', 'FIN', 'department']
        widgets = {
            'first_name' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : "Enter your first name",
                }
            ),
            'last_name' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : "Enter your last name"
                }
            ),
            'FIN' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : "Enter your FIN code"
                }
            ),
            'email' : forms.EmailInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"Enter your e-mail"
                }
            ),
            'number' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : "Enter your number"
                }
            ),
            'department' : forms.Select(
                attrs={
                    'class' : 'form-control',
                    'placeholder' :"- choose department -"
                }
            ),
        }




