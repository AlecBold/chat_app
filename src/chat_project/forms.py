from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import UserModel


class RegisterForm(UserCreationForm):

    class Meta:
        model = UserModel
        fields = ['username', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        if UserModel.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists.')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password.")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match.")
        return password2


class LoginForm(AuthenticationForm):

    class Meta:
        model = UserModel
        fields = ['username', 'password']
