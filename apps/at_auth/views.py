# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def forget_password(request):
    return HttpResponse('兄嘚，要啥自行车！')

# 登录页面
def login(request):
    return render(request, 'login/login.html')

# 登录动作
def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # 登录,并将session信息记录浏览器
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/auth/index/')
            return response
        else:
            return render(request, 'login/login.html', {'error': 'username or passwprd error!'})
    else:
        return render(request, 'login/login.html', {'error': 'username or passwprd error!'})

@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/auth/login/')
    return response


# 首页
@login_required
def index(request):
    username = request.session.get('user', '')
    user = User.objects.get(username=username)
    user_email = user.email
    return render(request, 'index.html', {'user': username, 'email': user_email})

def check_health(request):
    return HttpResponse("ok")


