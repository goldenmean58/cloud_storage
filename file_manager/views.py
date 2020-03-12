from django.shortcuts import render, redirect

from django.http import HttpResponse

# Create your views here.
from django.conf import settings

from filemanager import FileManager


def view(request, path):
    if request.user.is_authenticated:
        extensions = ['html', 'htm', 'zip', 'py', 'css', 'js', 'jpeg', 'jpg', 'png']
        username = request.user.username
        fm = FileManager(settings.MEDIA_ROOT + "/" + username, extensions=extensions)
        return fm.render(request, path)
    else:
        return redirect('/user/login')
