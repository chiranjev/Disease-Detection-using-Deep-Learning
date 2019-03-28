from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import keras

# from imutils import build_montages
# from imutils import paths
import numpy as np
import argparse
import random
import cv2
import shutil
import os
from .utils import *



model = load_model('media/models/malaria.model')
model._make_predict_function()
mod = load_model(settings.BASE_DIR+'\\media\\models\\dretinopathy.hd5')
mod._make_predict_function()

def index(request):
    return render(request, 'DiseaseDetectionApp/base.html',{})

def drprediction(p):
    mod.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    print('*************************************************1')
    test_gen = ImageDataGenerator(rescale = 1./255)
    import os
    print('*************************************************2')
    test_data = test_gen.flow_from_directory(settings.BASE_DIR+'\\DiseaseDetectionApp\\static\\DiseaseDetectionApp\\dretin',
                                              target_size = (64, 64),
                                              batch_size = 32,
                                              class_mode = 'binary', shuffle=False)
    filenames = test_data.filenames
    nb_samples = len(filenames)
    print('*************************************************3')
    predict = mod.predict_generator(test_data,steps = nb_samples/32)
    loss, acc = mod.evaluate_generator(test_data, steps=nb_samples/32, verbose=0)
    y_pred = predict[0][0] > 0.4
    print('*************************************************4')
    print(y_pred)
    percent_chance = round(predict[0][0]*100, 2)

    if y_pred == True:
        label = "Parasitized"
    else: label = "Uninfected"

    return label


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
            malaria_obj = Malaria.objects.filter().order_by('-pk')[0]
            malaria_obj.prediction = label
            if request.user.is_authenticated:
                user_obj = User.objects.get(username=request.user.username)
                malaria_obj.user = user_obj
            malaria_obj.save()
            return render(request, 'DiseaseDetectionApp/malaria.html', {'image_path': image_path,'label':label})

            return redirect('/malaria',{'image_path': image_path})
    else:
        form = MalariaForm()
    return render(request, 'DiseaseDetectionApp/malaria.html', {'form' : form})

def cancer(request):

    if request.method == 'POST':
        form = CancerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            image_path = form.cleaned_data['cancer_img']
            # print('kdslfjskldfjsdlkfjsdklfjsdflkj')
            # print(image_path)
            label = prediction('media/images/'+str(image_path))
            if(label=='Parasitized'):
                label = "has cancer"
            else:
                label = "does not have cancer"

            malaria_obj = Cancer.objects.filter().order_by('-pk')[0]
            malaria_obj.prediction = label
            if request.user.is_authenticated:
                user_obj = User.objects.get(username=request.user.username)
                malaria_obj.user = user_obj
            malaria_obj.save()

            return render(request, 'DiseaseDetectionApp/cancer.html', {'image_path': image_path,'label':label})

            return redirect('/cancer',{'image_path': image_path})
    else:
        form = CancerForm()
    return render(request, 'DiseaseDetectionApp/cancer.html', {'form' : form})

def retina(request):

    if request.method == 'POST':
        form = DiabeticRetinopathyForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            image_path = form.cleaned_data['retina_img']
            # print('kdslfjskldfjsdlkfjsdklfjsdflkj')
            # print(image_path)
            mydir = settings.BASE_DIR+'\\DiseaseDetectionApp\\static\\DiseaseDetectionApp\\dretin\\dataimages\\'
            if len(os.listdir(mydir)) != 0:
                filelist = [ f for f in os.listdir(mydir) if f.endswith(".jpeg") ]
                for f in filelist:
                    os.remove(os.path.join(mydir, f))

            if ('media/images/'+str(image_path)):
                src_dir = "media/images/"+str(image_path)
                dst_dir = mydir
                shutil.copy(src_dir, dst_dir)

            label = drprediction('media/images/'+str(image_path))
            if(label=='Parasitized'):
                label = "diabetic"
            else:
                label = "not diabetic"
            malaria_obj = DiabeticRetinopathy.objects.filter().order_by('-pk')[0]
            malaria_obj.prediction = label
            if request.user.is_authenticated:
                user_obj = User.objects.get(username=request.user.username)
                malaria_obj.user = user_obj
            malaria_obj.save()
            return render(request, 'DiseaseDetectionApp/retina.html', {'image_path': image_path,'label':label})

            return redirect('/retina',{'image_path': image_path})
    else:
        form = DiabeticRetinopathyForm()
    return render(request, 'DiseaseDetectionApp/retina.html', {'form' : form})

    # if request.method == 'POST':
    #     form = DiabeticRetinopathyForm(request.POST, request.FILES)
    #
    #     if form.is_valid():
    #         form.save()
    #         image_path = form.cleaned_data['retina_img']
    #         # print('kdslfjskldfjsdlkfjsdklfjsdflkj')
    #         # print(image_path)
    #         label = prediction('media/images/'+str(image_path))
    #         if(label=='Parasitized'):
    #             label = "has diabeties"
    #         else:
    #             label = "does not have diabeties"
    #
    #         malaria_obj = DiabeticRetinopathy.objects.filter().order_by('-pk')[0]
    #         malaria_obj.prediction = label
    #         if request.user.is_authenticated:
    #             user_obj = User.objects.get(username=request.user.username)
    #             malaria_obj.user = user_obj
    #         malaria_obj.save()
    #
    #
    #         return render(request, 'DiseaseDetectionApp/retina.html', {'image_path': image_path,'label':label})
    #
    #         return redirect('/retina',{'image_path': image_path})
    # else:
    #     form = DiabeticRetinopathyForm()
    # return render(request, 'DiseaseDetectionApp/retina.html', {'form' : form})


def index(request):
    return render(request, 'DiseaseDetectionApp/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        # profile_form = UserProfileInfoForm(data = request.POST)

        # Add profile form valid
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # profile = profile_form.save(commit=False)
            # profile.user = user

            # if 'profile_pic' in request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']

            # profile.save()

            registered = True
        else:
            # Add Profile Form errors
            print(user_form.errors)

    else:
        user_form = UserForm()
        # profile_form = UserProfileInfoForm()

    # Add Profile Form Dict
    return render(request, 'DiseaseDetectionApp/registration.html', {'user_form':user_form, 'registered':registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account Not Active!")
        else:
            print("Login and Failed!")
            print("Username: {} and Password: {}".format(username, password))
            return HttpResponse("Invalid Login Details Supplied!")
    else:
        return render(request, 'DiseaseDetectionApp/login.html', {})
