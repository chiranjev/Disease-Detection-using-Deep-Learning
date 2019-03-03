from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import *
from django.http import HttpResponse

from keras.preprocessing.image import img_to_array
from keras.models import load_model
from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import random
import cv2


def index(request):
    return render(request, 'DiseaseDetectionApp/base.html',{})

def prediction(p):
    orig = cv2.imread(p)


def malaria(request):

    if request.method == 'POST':
        form = MalariaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            image_path = form.cleaned_data['malaria_img']
            print('kdslfjskldfjsdlkfjsdklfjsdflkj')
            print(image_path)
            return render(request, 'DiseaseDetectionApp/malaria.html', {'image_path': image_path})

            return redirect('/malaria',{'image_path': image_path})
    else:
        form = MalariaForm()
    return render(request, 'DiseaseDetectionApp/malaria.html', {'form' : form})
