from app.models import User, Profile
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField

class LoginForm(forms.Form):
  username = forms.CharField(min_length=4)
  password = forms.CharField(min_length=4, widget=forms.PasswordInput)

  def clean_password(self):
    data = self.cleaned_data['password']
    if data == 'wrong':
      raise ValidationError('Wrong password')
    return data

class RegistrationForm(forms.ModelForm):
  password = forms.CharField(min_length=4, widget=forms.PasswordInput)
  confirm_password = forms.CharField(min_length=4, widget=forms.PasswordInput)
  avatar = forms.ImageField(required=False)

  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']

  def clean_confirm_password(self):
    password = self.cleaned_data['password']
    password_confirm = self.cleaned_data['confirm_password']
    if password != password_confirm:
      raise ValidationError('Passwords dont match')

    return password

  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data['password'])
    user.save()
    user_prof = Profile.objects.create(user=user)
    avatar = self.cleaned_data.get('avatar')
    if avatar:
      user_prof.avatar = avatar
    user_prof.save()
    return user

class SettingsForm(forms.ModelForm):
  bio = forms.CharField(widget=forms.Textarea, required=False)
  avatar = forms.ImageField(required=False)

  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']

  def save(self, commit=True):
    user = super().save()
    user_prof = Profile.objects.get(user=user)
    bio = self.cleaned_data.get('bio')
    avatar = self.cleaned_data.get('avatar')
    if avatar:
      user_prof.avatar = avatar
    if bio:
      user_prof.bio = bio

    user_prof.save()
    return user
