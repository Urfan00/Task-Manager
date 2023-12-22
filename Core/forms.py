from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


# Account Edit Form
class AccountEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['image', 'bio', 'number']
        widgets = {
            'image' : forms.ClearableFileInput(
                attrs={
                    'type' : 'file',
                    'class' : 'form-control',
                }
            ),
            'bio' : forms.Textarea(
                attrs={
                    'class' : 'form-control',
                    'rows' : 7
                }
            ),
            'number' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'type' : 'text'
                }
            )
        }
