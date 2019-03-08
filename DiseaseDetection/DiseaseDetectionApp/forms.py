from django import forms
from .models import *
from django.contrib.auth.models import User
from DiseaseDetectionApp.models import UserProfileInfo

class MalariaForm(forms.ModelForm):

    class Meta:
        model = Malaria
        fields = ['malaria_img']

class CancerForm(forms.ModelForm):

    class Meta:
        model = Cancer
        fields = ['cancer_img']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

# class UserProfileInfoForm(forms.ModelForm):
#     class Meta:
#         model = UserProfileInfo
#         fields = ('portfolio_site', 'profile_pic')
