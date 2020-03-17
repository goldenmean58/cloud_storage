from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from time import time
import hashlib
import os
from .models import File, DownloadLink
from django.core.files import File as DownloadFile
from django.utils import timezone
import datetime

def create_dir(user_name, current_dir, dir_name):
    if current_dir != "":
        parent = File.objects.filter(user_name=user_name, dir_name=current_dir, is_dir=True)
        if not parent:
            return False
        parent = parent.first()
        prefix = parent.dir_name
        parent_id = parent.id
    else:
        prefix = ""
        parent_id = -1
    if current_dir == "/":
        prefix = ""
    real_name = prefix + "/" + dir_name
    new_dir = File.objects.filter(user_name=user_name, dir_name=real_name, is_dir=True, file_name=dir_name)
    if not new_dir:
        new_dir = File(dir_name=real_name, user_name=user_name, parent_id=parent_id, is_shared=False, is_dir=True, file_name=dir_name)
        new_dir.save()
    return True

# Create your views here.
@csrf_exempt
def upload_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated:
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    os.makedirs('files', exist_ok=True)
    create_dir(request.user, "", '')
    current_dir = request.POST.get("current_dir", None)
    parent = File.objects.filter(user_name=request.user, dir_name=current_dir, is_dir=True)
    if not parent:
        return JsonResponse({'code': 30000, 'msg': 'No such a directory'})
    parent_id = parent.first().id
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
    file = File(file_name=file_name, file_size=file_size, md5=md5, blake2=blake2s, parent_id=parent_id, is_shared=False, shared_key='', user_name=request.user, is_dir=False, dir_name=current_dir + ("/" if current_dir != "/" else "") + file_name)
    file.save()
    return JsonResponse({"code": 0, "msg": "Upload successfully"})

def view(user, dir_name):
    current_dir = File.objects.filter(user_name=user, dir_name=dir_name)
    if not current_dir:
        return JsonResponse({'code': 30000, 'msg': 'No such a directory'})
    if current_dir.first().is_dir == True:
        current_dir = current_dir.first()
        parent_id = current_dir.id
        files = list(File.objects.filter(user_name=user, parent_id=parent_id, is_dir=False).values())
        dirs = list(File.objects.filter(user_name=user, parent_id=parent_id, is_dir=True).values())
        return JsonResponse({"code": 0, "files": files, "dirs": dirs})
    else:
        return JsonResponse({"code": 0, "file": list(current_dir.values())})

@csrf_exempt
def view_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    # if not request.user.is_authenticated:
    #     return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    os.makedirs('files', exist_ok=True)
    create_dir(request.user, "", '')
    path = request.POST.get("path", None)
    user = str(request.POST.get("user", request.user))
    key = request.POST.get("key", None) 
    if not key and user != str(request.user):
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    if user == str(request.user):
        return view(user, path)
    if not check_key(user, path, key):
        return JsonResponse({'code': 30000, 'msg': 'No such a directory'})
    return view(user, path)

def check_key(user, path, key):
    request_path = File.objects.filter(user_name=user, dir_name=path)
    if not request_path:
        return False
    parent_id = request_path.first().id
    while(True):
        check_dir = File.objects.filter(user_name=user, id=parent_id)
        if not check_dir:
            return False
        check_dir = check_dir.first()
        if check_dir.dir_name == "/":
            valid = False
            break
        parent_id = check_dir.parent_id
        if check_dir.shared_key == key and check_dir.shared_expire_time >= timezone.now():
            valid = True
            break
    if not valid:
        return False
    return True

@csrf_exempt
def get_download_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    # if not request.user.is_authenticated:
    #     return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    user = request.POST.get("user", None)
    path = request.POST.get("path", None)
    key = request.POST.get("key", "")
    if not user or not path:
        return JsonResponse({'code': 30000, 'msg': 'Missing Parameters'})
    if user != str(request.user) and key is None:
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    if user != str(request.user) and not check_key(user, path, key):
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    dir_name = path[:path.rfind('/')]
    dir_name = "/" if dir_name == "" else dir_name
    base_name = path[path.rfind('/')+1:]
    parent = File.objects.filter(dir_name=dir_name, user_name=user)
    if not parent:
        return JsonResponse({'code': 30000, 'msg': 'No such a file'})
    parent = parent.first()
    download_file = File.objects.filter(user_name=user, parent_id=parent.id, file_name=base_name)
    if not download_file:
        return JsonResponse({'code': 30000, 'msg': 'No such a file'})
    download_file = download_file.first()
    link = download_file.md5 + download_file.blake2 + str(int(time()))
    download_link = DownloadLink(md5=download_file.md5, blake2=download_file.blake2, link=link, file_name=base_name)
    download_link.save()
    return JsonResponse({"code": 0, "link": link})

@csrf_exempt
def download_view(request, link):
    download_link = DownloadLink.objects.filter(link=link, create_time__gt=timezone.now() - datetime.timedelta(days=7))
    if not download_link:
        return HttpResponseNotFound()
    download_link = download_link.first()
    file_path = 'files/' + download_link.md5 + download_link.blake2
    f = open(file_path, 'rb')
    myfile = DownloadFile(f)
    response = HttpResponse(myfile, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + download_link.file_name
    return response

@csrf_exempt
def move_view(request):
    pass

@csrf_exempt
def copy_view(request):
    pass

def delete(username, parent_id, id_itself, is_dir):
    if not is_dir:
        is_file = File.objects.filter(user_name=username, id=id_itself)
        if not is_file:
            return False
        delete_file = is_file.first()
        os.remove('files/' + delete_file.md5 + delete_file.blake2)
        is_file.delete()
        return True
    is_dir = File.objects.filter(user_name=username, id=id_itself)
    dir_info = is_dir.first()
    files_inside = File.objects.filter(user_name=username, parent_id=dir_info.id)
    for file in files_inside:
        if not delete(username, dir_info.id, file.id, False):
            return False
    dirs_inside = File.objects.filter(user_name=username, parent_id=dir_info.id)
    for dir in dirs_inside:
        if not delete(username, dir_info.id, dir.id, True):
            return False
    is_dir.delete()
    return True

@csrf_exempt
def delete_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated:
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    os.makedirs('files', exist_ok=True)
    create_dir(request.user, "", '')
    current_dir = request.POST.get("current_dir", None)
    file_name = request.POST.get("file_name", None)
    current_dir = File.objects.filter(user_name=request.user, dir_name=current_dir)
    if not file_name or not current_dir:
        return JsonResponse({'code': 30000, 'msg': 'Missing Parameters'})
    parent_id = current_dir.first().id
    delete_file = File.objects.filter(user_name=request.user, parent_id=parent_id, file_name=file_name)
    parent_name = current_dir.first().dir_name
    parent_name = "" if parent_name == "/" else parent_name
    delete_dir = File.objects.filter(user_name=request.user, parent_id=parent_id, dir_name=parent_name + "/" + file_name)
    if not delete_file and not delete_dir:
        return JsonResponse({'code': 30001, 'msg': 'Cannot delete that file or directory'})
    is_dir = not delete_file
    delete_id = delete_dir.first().id if is_dir else delete_file.first().id
    if not delete(request.user, parent_id, delete_id, is_dir):
        return JsonResponse({'code': 30001, 'msg': 'Cannot delete that file or directory'})
    return JsonResponse({"code": 0, "msg": "Delete successfully"})


@csrf_exempt
def share_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated:
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    os.makedirs('files', exist_ok=True)
    create_dir(request.user, "", '')
    current_dir = request.POST.get("current_dir", None)
    file_name = request.POST.get("file_name", None)
    shared_key = request.POST.get("key", "")
    share_day = int(request.POST.get("day", 7))
    if not file_name or not current_dir:
        return JsonResponse({'code': 30000, 'msg': 'Missing Parameters'})
    parent = File.objects.filter(user_name=request.user, dir_name=current_dir)
    if not parent:
        return JsonResponse({'code': 30000, 'msg': 'No such a directory'})
    parent_id = parent.first().id
    parent_name = "" if current_dir == "/" else current_dir
    print(parent_name+"/"+file_name)
    print(parent_id)
    share = File.objects.filter(user_name=request.user, parent_id=parent_id, dir_name=parent_name + "/" + file_name)
    if not share:
        return JsonResponse({'code': 30001, 'msg': 'Cannot share that file or directory'})
    share.update(is_shared=True, shared_key=shared_key, shared_expire_time=timezone.now() + datetime.timedelta(days=share_day))
    return JsonResponse({"code": 0, "msg": "Share successfully", "share_url": "view/" + str(request.user) + parent_name + "/" + file_name, "shared_key": shared_key})



@csrf_exempt
def unshare_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated:
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    os.makedirs('files', exist_ok=True)
    create_dir(request.user, "", '')
    current_dir = request.POST.get("current_dir", None)
    file_name = request.POST.get("file_name", None)
    current_dir = File.objects.filter(user_name=request.user, dir_name=current_dir)
    if not file_name or not current_dir:
        return JsonResponse({'code': 30000, 'msg': 'Missing Parameters'})
    parent_id = current_dir.first().id
    unshare_file = File.objects.filter(user_name=request.user, parent_id=parent_id, file_name=file_name)
    parent_name = current_dir.first().dir_name
    parent_name = "" if parent_name == "/" else parent_name
    unshare_dir = File.objects.filter(user_name=request.user, parent_id=parent_id, dir_name=parent_name + "/" + file_name)
    if not unshare_file and not unshare_dir:
        return JsonResponse({'code': 30001, 'msg': 'Cannot unshare that file or directory'})
    if not unshare_file:
        unshare_dir.update(is_shared=False)
    else:
        unshare_file.update(is_shared=False)
    return JsonResponse({"code": 0, "msg": "Unshare successfully"})

@csrf_exempt
def create_dir_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated:
        return JsonResponse({'code': 20000, 'msg': "Not authenticated user"})
    os.makedirs('files', exist_ok=True)
    create_dir(request.user, "", '')
    current_dir = request.POST.get("current_dir", None)
    dir_name = request.POST.get("dir_name", None)
    if not current_dir or not dir_name:
        return JsonResponse({'code': 30000, 'msg': 'No such a directory'})
    if create_dir(request.user, current_dir, dir_name):
        return JsonResponse({"code": 0, "msg": "Create directory successfully"})
    return JsonResponse({"code": 30002, "msg": "Failed tocreate directory successfully"})


