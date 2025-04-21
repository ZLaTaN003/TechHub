from django import forms


class SignUp(forms.Form):
    username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={"label":"","placeholder":"Name"}))
    password1 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"label":"","placeholder":"Password"}))
    password2 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"label":"","placeholder":"Confirm Password"}))

class Login(forms.Form):
    username = forms.CharField(max_length=200,required=True,widget=forms.TextInput(attrs={"label":"","placeholder":"Name"}))
    password = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"label":"","placeholder":"Password"}),required=True)