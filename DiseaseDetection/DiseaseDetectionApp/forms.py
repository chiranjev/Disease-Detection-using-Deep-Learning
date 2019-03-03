from django import forms
from .models import *

class MalariaForm(forms.ModelForm):

    class Meta:
        model = Malaria
        fields = ['malaria_img'] 
