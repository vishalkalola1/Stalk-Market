from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from .forms import LoginForm, RegisterForm, UploadFileForm
from .models import UserCustom,UploadFile
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User,auth

import os
from google.cloud import vision
from google.cloud.vision import types
import requests
import base64

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'pristockmarket.json'

def home(request):
    context = {}
    if request.method == "POST":
        print("Test")
    else:
        return render(request, 'BrandAnalysisApp/index.html', context)


def login(request):
    context = {}
    if request.method == "POST":
        username = request.POST['uemail']
        password = request.POST['upassword']
        try:
            user = UserCustom.objects.get(uemail=username)
            if user.uemail == username and user.upassword == password:
                if user.utype == "Admin":
                    return HttpResponseRedirect(reverse("home"))
                else:
                    return HttpResponseRedirect(reverse("uploadImage"))
            else:
                context["error"] = "User is not authenticated"
                return render(request, 'BrandAnalysisApp/SignIn.html', context)
        except:
            context["error"] = "User is not register with this email id"
            return render(request, 'BrandAnalysisApp/SignIn.html', context)
    else:
        userform = LoginForm()
        context["form"] = userform
        return render(request,'BrandAnalysisApp/SignIn.html',context)

def register(request):
    context = {}
    if request.method == "POST":
        username = request.POST['uemail']
        password = request.POST['upassword']
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            registerform.save()
            return HttpResponseRedirect(reverse("uploadImage"))
        else:
            context["error"] = "Email already register."
            return render(request,'BrandAnalysisApp/Register.html',context)
    else:
        userform = RegisterForm()
        context["form"] = userform
        return render(request,'BrandAnalysisApp/Register.html',context)

def uploadImage(request):
    context = {}
    if request.method == "POST":
        imageForms = UploadFileForm(request.POST, request.FILES)
        if imageForms.is_valid():
            files = imageForms.files.getlist('file')
            for i in range(len(files)):
                file = files[i]
                handle_uploaded_file(file, file.name)
        else:
            context["error"] = "File not uploaded try again later"
        context["error"] = "Image uploaded successfully"
        return render(request, 'BrandAnalysisApp/UploadImage.html',context)
    else:
        return render(request, 'BrandAnalysisApp/UploadImage.html',context)

def handle_uploaded_file(f,name):
    encoded_string = base64.b64encode(f.read()).decode('UTF-8')
    # callgoogleVisionAPi(encoded_string)

    filename_w_ext = os.path.basename(name)
    path = '/Users/vishal/Documents/Projects/PRI/BrandAnalysis/BrandAnalysisApp/Media/' + filename_w_ext
    print(path)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def callgoogleVisionAPi(obj):
    url = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaSyDjL9v7LlXtC2gnr4wu8SvOHGa70Ej25UI'
    data = { "requests": [{ "image": { "content": obj }, "features": [{"maxResults": 10, "type": "OBJECT_LOCALIZATION"},]}]}
    print(data)
    response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
    print(response)



