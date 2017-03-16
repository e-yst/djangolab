from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from main.models import *
from main.forms import LoginForm, RegisterForm

# Create your views here.


def login_page(request):
    if request.user.is_authenticated():
        return redirect('event_list')

    form = LoginForm(request.POST or None)
    register_url  = 'http://' + request.META['HTTP_HOST'] + '/register'
    profile_url  = 'http://' + request.META['HTTP_HOST'] + '/profile'
    if 'HTTP_REFERER' in request.META.keys():
        referer = request.META['HTTP_REFERER']
    else:
        referer = None

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('event_list')
                else:
                    error = '你的帳號已被停用!'
                    return render(request, 'login.html',
                                  {'form': form,
                                   'error': error})
            else:
                error = '帳號或密碼錯誤!'
                return render(request, 'login.html',
                              {'form': form,
                               'error': error})
        else:
            return render(request, 'login.html', {'form': form})

    elif request.method == 'GET' and referer == register_url:
        message = '成功註冊，請輸入帳密登入！'
        return render(request, 'login.html',
                      {'form': form,
                       'message': message})
    elif request.method == 'GET' and referer == profile_url:
        message = '已更改密碼，請重新登入！'
        return render(request, 'login.html',
                      {'form': form,
                       'message': message})
    else:
        return render(request, 'login.html', {'form': form})


@login_required
def logout_page(request):
    logout(request)
    return render(request, 'logout.html')

def register(request):
    form = RegisterForm(request.POST or None)
    if request.user.is_authenticated():
        return redirect('event_list')
    elif request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            username_error = []
            email_error = []
            pwd_error = []
            cpwd_error = []

            if len(username) == 0:
                username_error.append('這個欄位是必要的！')
            elif len(username) > 0:
                try:
                    User.objects.get(username=username)
                    username_error.append('%s 已被使用！' % username)
                    print('username_error')
                except:
                    pass

            if len(email) == 0:
                email_error.append('這個欄位是必要的！')
            elif len(email) > 0:
                try:
                    User.objects.get(email=email)
                    email_error.append('%s 已被使用！' % email)
                except:
                    pass
                if 'mail.ntust.edu.tw' not in email.lower():
                    email_error.append('請使用台科大的電子郵箱註冊！')

            if len(password) == 0:
                pwd_error.append('這個欄位是必要的！')
            elif len(password) > 0 and len(confirm_password) > 0:
                if password != confirm_password:
                    pwd_error.append('密碼不一致！')

            if len(confirm_password) == 0:
                cpwd_error.append('這個欄位是必要的！')
            elif len(confirm_password) and len(password)> 0:
                if password != confirm_password:
                    cpwd_error.append('密碼不一致！')

            if len(username_error) + len(email_error) +\
               len(pwd_error) + len(cpwd_error) == 0:
                User.objects.create_user(
                    username, email, password)
                return redirect('login')

            return render(request, 'register.html',
                            {'form': form,
                             'username_error': username_error,
                             'email_error': email_error,
                             'pwd_error': pwd_error,
                             'cpwd_error': cpwd_error})
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

def password_reset(request):
    pass


def password_reset_done(request):
    pass
