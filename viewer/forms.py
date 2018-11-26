from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from controller.models import Profile


# user signup form
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


# user profile form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'theme', 'active', 'trash')
