from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    if not username or not password:
        return HttpResponseBadRequest()
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"code": 0, "msg": "Login successfully"})
    return JsonResponse({"code": 10000, "msg": "Failed to login"})

@csrf_exempt
def register_view(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    if not request.user.is_authenticated:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if not username or not password:
            return HttpResponseBadRequest()
        has_user = User.objects.filter(username=username)
        if has_user:
            return JsonResponse({"code": 30000 , "msg": "User has existen, failed to register "})
        user = User.objects.create_user(username=username, password=password)
        user.save()
    return JsonResponse({"code": 0 , "msg": "Register successfully"})

@csrf_exempt
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({"code": 0, "msg": "Logout successfully"})
