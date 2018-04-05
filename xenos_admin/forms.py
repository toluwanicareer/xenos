from django import forms
from django.contrib.auth.models import User
from acc.models import Profile
from .models import Post, xenos_payment

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('username','first_name','last_name','email')

        widgets={
        'first_name':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'last_name':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'username':forms.TextInput(attrs={'class':'form-control borderprob'}),
        'email':forms.EmailInput(attrs={'class':'form-control borderprob'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('passport','phone', 'id_image')

        widgets={
        'phone':forms.TextInput(attrs={'class':'form-control'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title', 'text')

        




class XenosForm(forms.ModelForm):
    class Meta:
        model=xenos_payment
        fields=('bot',)

        


        

