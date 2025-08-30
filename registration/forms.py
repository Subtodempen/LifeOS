from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", max_length=100)

class SignupForm(LoginForm):
    firstName = forms.CharField(label="firstName", max_length=100)
    lastName = forms.CharField(label="lastName", max_length=100)
