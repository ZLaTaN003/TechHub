from django import forms
from django.forms import ModelForm
from .models import ProductComment

class SignUp(forms.Form):
    username = forms.CharField(max_length=200,widget=forms.TextInput(attrs={"label":"","placeholder":"Name"}))
    password1 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"label":"","placeholder":"Password"}))
    password2 = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"label":"","placeholder":"Confirm Password"}))

class Login(forms.Form):
    username = forms.CharField(max_length=200,required=True,widget=forms.TextInput(attrs={"label":"","placeholder":"Name"}))
    password = forms.CharField(max_length=200,widget=forms.PasswordInput(attrs={"label":"","placeholder":"Password"}),required=True)

class ProductCommentForm(ModelForm):
    class Meta:
        model = ProductComment
        fields = ["comment"]
    def __init__(self,*args,**kwargs):
        super().__init__(*args,*kwargs)
        self.fields["comment"].widget.attrs.update({"class":"commentform"})
  
