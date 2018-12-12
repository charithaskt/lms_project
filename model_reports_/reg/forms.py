from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
User = get_user_model()

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('fullname', 'email', 'password1', 'password2')




class LoginForm(forms.Form):
    email = forms.CharField(widget= forms.EmailInput
                           (attrs={'class':'input',
				   'id':'user'}))
    password = forms.CharField(widget= forms.PasswordInput
                           (attrs={'class':'input',
				   'id':'pass'}))
