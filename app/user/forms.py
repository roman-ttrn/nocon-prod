from django import forms
from django.contrib.auth.models import User
from .models import Profile

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Имя пользователя', 'class': 'input-field'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'input-field'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'file-input'}),
        }

