from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import time
import hashlib
import os
from .models import Dir, File, DownloadLink

def create_dir(user_name, dir_name):
    root_dir = Dir.objects.filter(user_name=user_name, dir_name=dir_name)
    if not root_dir:
        root_dir = Dir(dir_name=dir_name, user_name=user_name, parent_id=-1)
        root_dir.save()

# Create your views here.
@csrf_exempt
def upload_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated:
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    os.makedirs('files', exist_ok=True)
    create_dir(request.user, '/')
    current_dir = request.POST.get("current_dir", None)
    current_dir = Dir.objects.filter(user_name=request.user, dir_name=current_dir)
    if not current_dir:
        return JsonResponse({'code': 30000, 'msg': 'No such a directory'})
    parent_id = current_dir.first().id
    file_name = request.FILES['file'].name
    file_size = request.FILES['file'].size
    md5 = hashlib.md5()
    blake2s = hashlib.blake2s()
    tmp_real_name = 'files/' + file_name + str(int(time()))
    with open(tmp_real_name, "wb+") as f:
        for chunk in request.FILES['file'].chunks():
            md5.update(chunk)
            blake2s.update(chunk)
            f.write(chunk)
    md5 = md5.hexdigest()
    blake2s  = blake2s.hexdigest()
    real_name = 'files/' + md5 + blake2s
    os.rename(tmp_real_name, real_name)
    file = File(file_name=file_name, file_size=file_size, md5=md5, blake2=blake2s, parent_id=parent_id, is_shared=False, shared_key='', user_name=request.user)
    file.save()
    return JsonResponse({"code": 0, "msg": "Upload successfully"})

@csrf_exempt
def view_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated:
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    os.makedirs('files', exist_ok=True)
    create_dir(request.user, '/')
    current_dir = request.POST.get("current_dir", None)
    current_dir = Dir.objects.filter(user_name=request.user, dir_name=current_dir)
    if not current_dir:
        return JsonResponse({'code': 30000, 'msg': 'No such a directory'})
    parent_id = current_dir.first().id
    files = list(File.objects.filter(user_name=request.user, parent_id=parent_id).values())
    return JsonResponse({"code": 0, "data": files})

@csrf_exempt
def download_view(request):
    pass

@csrf_exempt
def move_view(request):
    pass

@csrf_exempt
def copy_view(request):
    pass

@csrf_exempt
def delete_view(request):
    pass

@csrf_exempt
def share_view(request):
    pass

@csrf_exempt
def unshare_view(request):
    pass

@csrf_exempt
def create_dir_view(request):
    pass
