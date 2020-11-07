from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from . import models


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label="Email", max_length=255)

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = models.User.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Username {username} is already in use.")

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = models.User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")


class LoginForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid username")

