from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core import serializers
import json


@csrf_exempt
def login(request):
    json_data = json.loads(request.body.decode("utf-8"))
    if request.POST or json_data:
        username = request.POST.get('username') or json_data.get('username')
        password = request.POST.get('password') or json_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return HttpResponse(json.dumps({"result": True, "username": request.user.username}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"result": False}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"result": False}), content_type="application/json")


@csrf_exempt
def v_logout(request):
    auth_logout(request)
    return HttpResponse(json.dumps({"result": True}), content_type="application/json")


@csrf_exempt
def register(request):
    json_data = json.loads(request.body.decode("utf-8"))
    if request.POST or json_data:
        username = request.POST.get('username') or json_data.get('username')
        password = request.POST.get('password') or json_data.get('password')
        user = User.objects.create_user(username=username,password=password)
        return HttpResponse(json.dumps({"result": True}), content_type="application/json")


@csrf_exempt
def getProfile(request):
    if request.user.is_authenticated:
        return HttpResponse(json.dumps({"username": request.user.username, "isAdmin": request.user.is_superuser}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"username": "", "isAdmin": False}), content_type="application/json")
