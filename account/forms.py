from django import forms

class UpdateUserForm(forms.Form):
    firstname = forms.CharField(label='Your name', max_length=15)
    middlename = forms.CharField(label='Your name', max_length=15)
    lastname = forms.CharField(label='Your name', max_length=15)