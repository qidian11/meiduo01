from django.shortcuts import render
from django import http
from django.views import View
from django_redis import get_redis_connection

from meiduo_mall.libs.captcha.captcha import captcha

import re
from random import randint


# Create your views here.
class ImageCodeView(View):
    def get(self,request,uuid):
        # 1.获取图片验证码的值与图片
        _,text,image_data = captcha.generate_captcha()
        print(text)
        print(image_data)
        # 2.将图片验证码的值与uuid存入redis
        redis_conn = get_redis_connection('code')
        redis_conn.set(uuid,text,60)
        return http.HttpResponse(image_data,content_type='image/jpg')


class SmsCodeView(View):
    def get(self,request,mobile):
        # 1.获取参数
        image_code = request.GET.get('image_code')
        image_code_id = request.GET.get('image_code_id')
        print(image_code,image_code_id)
        # 2.校验参数
        if not all([image_code,image_code_id]):
            return http.HttpResponseForbidden('参数错误')
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return http.HttpResponseForbidden('手机号格式错误')

        # 3.检验验证码
        redis_conn = get_redis_connection('code')
        image_text = redis_conn.get(image_code_id)
        if image_text:
            print(image_text)
            if image_code.upper() != image_text.decode().upper():
                return http.HttpResponseForbidden('图片验证码错误')
        else:
            return http.HttpResponseForbidden('图片验证码错误')
        sms_code = randint(0,999999)
        sms_code = '%06d'%sms_code
        redis_conn.set(mobile,sms_code)
        return http.JsonResponse({'code':0,'sms_code':sms_code})