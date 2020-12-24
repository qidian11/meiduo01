from django.shortcuts import render,redirect
from django.views import View
from django import http

from django_redis import get_redis_connection

from .models import User
# Create your views here.

import re

class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        user_name = request.POST.get("user_name")
        pwd = request.POST.get("pwd")
        cpwd = request.POST.get("cpwd")
        mobile = request.POST.get("phone")
        msg_code = request.POST.get("msg_code")
        allow = request.POST.get("allow")

        # 2, 校验参数
        # 2,1 为空校验
        if not all([user_name, pwd, cpwd, mobile, msg_code, allow]):
            return http.HttpResponseForbidden("参数不全")

        # 2,2 两次密码一致
        if pwd != cpwd:
            return http.HttpResponseForbidden("两次密码不一致")

        # 2,3 手机号格式正确
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden("手机号格式有误")

        # 2,5 短信验证码正确(下一次完成)
        redis_conn = get_redis_connection("code")
        redis_sms_code = redis_conn.get(mobile)
        if msg_code != redis_sms_code.decode():
            return http.HttpResponseForbidden("短信验证码填写错误")

        # 2,6 协议需要同意
        if allow != 'on':
            return http.HttpResponseForbidden("协议需要同意")

        # 3, 数据入库
        # user = User.objects.create(username=user_name,password=pwd,mobile=phone)
        # 可以对密码加密
        user = User.objects.create_user(username=user_name, password=pwd, mobile=mobile)

        # 4, 返回响应
        return redirect('/')