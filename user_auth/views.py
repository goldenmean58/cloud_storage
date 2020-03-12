from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import os

# Create your views here.
def login_view(request):
    if request.method != 'POST' or not request.POST:
        return render(request, "login.html")
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/files/')
    return redirect('/user/login')

def register_view(request):
    if request.method != 'POST' or not request.POST:
        return render(request, "register.html")
    if not request.user.is_authenticated:
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = User.objects.create_user(username=username, password=password)
        user.save()
        os.mkdir('./storage/' + username)
    return redirect('/user/login')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return HttpResponseRedirect('/files')
