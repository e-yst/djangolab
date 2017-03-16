from datetime import datetime

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from main.models import *
from pytz import timezone as tz


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': '帳號'}),
        max_length=50)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '密碼'}))


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': '帳號'}),
        required=False)

    email = forms.CharField(
        widget=forms.EmailInput(attrs={'class': 'form-control',
                                       'placeholder': '電郵地址'}),
        required=False)

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '密碼'}),
        required=False)

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '確認密碼'}),
        required=False)


class ResetPwdForm(forms.Form):

    current_pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '目前密碼'}),
        required=True)

    new_pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '新密碼'}),
        required=True)

    confirm_pwd = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control',
                                          'placeholder': '確認新密碼'}),
        required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(ResetPwdForm, self).__init__(*args, **kwargs)

    def clean(self):
        current_pwd = self.cleaned_data['current_pwd']
        new_pwd = self.cleaned_data['new_pwd']
        confirm_pwd = self.cleaned_data['confirm_pwd']

        validate_pwd = authenticate(username=self.request.user.username,
                                    password=current_pwd)

        if validate_pwd == None:
            msg = '密碼不正確'
            self.add_error('current_pwd', msg)

        if new_pwd != confirm_pwd:
            msg = '密碼不一致！'
            self.add_error('new_pwd', msg)
            self.add_error('confirm_pwd', msg)


class NewEventForm(forms.Form):
    e_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': '請輸入活動名稱'}),
        max_length=255,
        required=True)

    e_startdate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control date',
                                      'placeholder': '請按這裡選擇時間'}),
        required=True)

    e_enddate = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control date',
                                      'placeholder': '請按這裡選擇時間'}),
        required=True)

    e_place = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': '請輸入地點'}),
        required=True)

    e_description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': '活動內容簡介'}),
        required=False)

    e_deadline = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control date',
                                      'placeholder': '報名截止日期'}),
        required=True)

    def clean(self):
        startdate = datetime.strptime(self.cleaned_data['e_startdate'],
                                      '%Y/%m/%d %I:%M %p')
        startdate = startdate.replace(tzinfo=tz('Asia/Taipei'))

        enddate = datetime.strptime(self.cleaned_data['e_enddate'],
                                    '%Y/%m/%d %I:%M %p')
        enddate = enddate.replace(tzinfo=tz('Asia/Taipei'))

        deadline = datetime.strptime(self.cleaned_data['e_deadline'],
                                     '%Y/%m/%d %I:%M %p')
        deadline = deadline.replace(tzinfo=tz('Asia/Taipei'))

        if timezone.localtime(timezone.now()) > startdate:
            msg = '活動開始日期必須在今天之後！'
            self.add_error('e_startdate', msg)

        if timezone.localtime(timezone.now()) > deadline:
            msg = '截止報名日期必須在今天之後！'
            self.add_error('e_deadline', msg)

        if timezone.localtime(timezone.now()) > enddate:
            msg = '活動結束日期必須在今天之後！'
            self.add_error('e_enddate', msg)

        if deadline > startdate:
            msg = '截止報名日期必須在活動開始日期之前！'
            self.add_error('e_deadline', msg)

        if startdate > enddate:
            msg = '活動開始日期必須在結束日期之前！'
            self.add_error('e_startdate', msg)

        if enddate < startdate:
            msg = '活動結束日期必須在開始日期之後！'
            self.add_error('e_enddate', msg)

        if enddate < deadline:
            msg = '活動結束日期必須在截止報名日期之後！'
            self.add_error('e_enddate', msg)


class HiddenForm(forms.Form):
    hidden_data = forms.CharField(widget=forms.HiddenInput())
    eventid = forms.CharField(widget=forms.HiddenInput())
