from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image
from keras.preprocessing import image
import numpy as np
import cv2

import tensorflow as tf
from keras.models import load_model
import keras.backend as K


global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0


camera = cv2.VideoCapture(0)

output_classes = {'Heart': 0, 'Oblong': 1, 'Oval': 2, 'Round': 3, 'Square': 4}

def cam(request):
    print("camera")
    return render(request,'index2.html')


def index(request):
    if request.method == 'POST':
        if 'myfile' not in request.FILES:
            print('a')
            return HttpResponseRedirect(reverse('index'))

        elif request.FILES['myfile']:

            print('b')
            myfile = request.FILES['myfile']
            print(myfile.name)
            fs = FileSystemStorage()

            print(fs)
            filename = fs.save(myfile.name, myfile)
            m = str(filename)
            K.clear_session()

            im = Image.open("{}/".format(settings.MEDIA_ROOT) + m)

            # You don't have to change this resolution, it is just to display on the screen
            j = im.resize((224, 224),)
            l = "predicted.jpg"
            j.save("{}/".format(settings.MEDIA_ROOT) + l)
            file_url = fs.url(l)	
            
            model = load_model('covidApp/modelnew1.hdf5', compile=False)

            # Change this target_size as per your trained resolution
            img = image.load_img(myfile, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            pred = model.predict(x).flatten()
            pred_class = np.argmax(pred)

            if pred_class == 0:
                prediction = 'Heart'
            elif pred_class == 1:
                prediction = 'oblong'
            elif pred_class == 2:
                 prediction = 'oval'
            elif pred_class == 3:
                prediction = 'Round'
            else:
                prediction= 'Square'
            #predicted_category = output_classes[pred_class]
            #predicted_category = output_classes[pred_class]

            return render(request, "index.html", {'result': prediction, 'file_url': file_url})

    return render(request, "index.html")

def aboutus(request):
    return render(request, 'aboutus.html')