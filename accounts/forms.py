from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from . import models

class signupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model : models.CustomUser
        fields = ('username','email',)