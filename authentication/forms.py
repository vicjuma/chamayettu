from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import User

class RegisterForm(UserCreationForm):
  email = forms.EmailField(
    required=True, widget=forms.TextInput(
      attrs={'placeholder': 'Email', 'class': 'form-control', 'id': 'email',}))
  
  phone_number = PhoneNumberField(
    widget = PhoneNumberPrefixWidget(
      initial='KE', attrs={
        'placeholder': '+254712345678', 'class': 'form-control', 'id': 'phone_number',})
  )
  
  phone_number1 = PhoneNumberField(
    widget = PhoneNumberPrefixWidget(
      initial='KE', attrs={
        'placeholder': '+254712345678', 'class': 'form-control', 'id': 'phone_number1',})
  )
  
  password1 = forms.CharField(
    max_length=50, required=True, widget=forms.PasswordInput(
      attrs={
        'placeholder': 'Password', 'class': 'form-control', \
          'data-toggle': 'password', 'id': 'password', }))
  
  password2 = forms.CharField(
    max_length=50, required=True,  widget=forms.PasswordInput(
      attrs={
        'placeholder': 'Confirm Password', 'class': \
          'form-control', 'data-toggle': 'toggleConfirmPassword', \
            'id': 'confirmPassword',}))
  
  accept_terms = forms.BooleanField(
    required=True)
  
  class Meta:
      model = User
      fields = [
       'email', 'phone_number', 'phone_number1', 'password1', 'password2', \
            'accept_terms']
  
  def clean_confirm_phone(self):
    phone_number = self.cleaned_data.get("phone")
    phone_number1 = self.cleaned_data.get("confirm_phone")

    if phone_number and phone_number1 and phone_number != phone_number1:
      raise forms.ValidationError("The two password fields must match.")
    return phone_number1
  
  def clean_confirm_password(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")

    if password1 and password2 and password1 != password2:
      raise forms.ValidationError("The two password fields must match.")
    return password2

  
class LoginForm(AuthenticationForm):
    username = PhoneNumberField(
    widget = PhoneNumberPrefixWidget(
      initial='KE', attrs={
        'placeholder': '+254712345678', 'class': 'form-control', 'id': 'phone_number1',})
  )
    
    password = forms.CharField(
      max_length=50, required=True, widget=forms.PasswordInput(
        attrs={
          'placeholder': 'Password', 'class': 'form-control', \
            'data-toggle': 'password', 'id': 'password', \
              'name': 'password',}))
    
    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']