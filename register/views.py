from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .form import RegisterForm

# Create your views here.

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST) # 
        if form.is_valid():
            form.save() # save the user data in database
        return redirect("/") # redirected to /home once registered
    else:
        form = RegisterForm() #blank form if not getting post request.

    return render(response,"register/register.html", {"form":form}) #the render is like that because of the simple urls

def profile(response):
    if response.method == "POST":
        pass
    return render(response, "register/profile.html", {})

