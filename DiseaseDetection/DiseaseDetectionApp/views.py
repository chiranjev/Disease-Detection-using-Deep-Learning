from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import *
from django.http import HttpResponse

from keras.preprocessing.image import img_to_array
from keras.models import load_model
# from imutils import build_montages
# from imutils import paths
import numpy as np
import argparse
import random
import cv2
from .utils import *



model = load_model('media/models/malaria.model')
model._make_predict_function()
def index(request):
    return render(request, 'DiseaseDetectionApp/base.html',{})

def prediction(p):
    orig = cv2.imread(p)
    print(p)
    print('lksdfjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
    image = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (64, 64))
    print(image)
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    print(image)
    print(model)
    print('------------')
    # make predictions on the input image
    pred = model.predict(image)
    pred = pred.argmax(axis=1)[0]

    # an index of zero is the 'parasitized' label while an index of
    # one is the 'uninfected' label
    label = "Parasitized" if pred == 0 else "Uninfected"
    color = (0, 0, 255) if pred == 0 else (0, 255, 0)

    return label
    # resize our original input (so we can better visualize it) and
    # then draw the label on the image
    # orig = cv2.resize(orig, (128, 128))
    # cv2.putText(orig, label, (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    # 	color, 2)


def malaria(request):

    if request.method == 'POST':
        form = MalariaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            image_path = form.cleaned_data['malaria_img']
            # print('kdslfjskldfjsdlkfjsdklfjsdflkj')
            # print(image_path)
            label = prediction('media/images/'+str(image_path))
            return render(request, 'DiseaseDetectionApp/malaria.html', {'image_path': image_path,'label':label})

            return redirect('/malaria',{'image_path': image_path})
    else:
        form = MalariaForm()
    return render(request, 'DiseaseDetectionApp/malaria.html', {'form' : form})
