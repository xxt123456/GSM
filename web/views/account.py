from io import BytesIO
from django.shortcuts import HttpResponse,render,redirect
from utils.check_code import create_validate_code
from repository import models
from ..forms.account import LoginForm
import json

def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img,code = create_validate_code()
    img.save(stream,'PNG')
    request.session['CheckCode']=code
    return HttpResponse(stream.getvalue())

def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method=='POST':
        result = {'status':False,'message':None,'data':None}
        form = LoginForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            we= models.UserInfo.objects.all()
            print(we)
            user_info = models.UserInfo.objects.filter(username=username,password=password).values('username','password','blog__nid').first()
            print(user_info)
            if not user_info:
                result['message']='用户名或密码错误'
            else:
                result['status'] = True
                request.session['user_info']=user_info
                if form.cleaned_data.get('rmb'):
                    request.session.set_expiry(60*60*24)
                # return render(request,'home.html')
        else:
            if 'check_code' in form.errors:
                result['message']='验证码过期'
            else:
                result['message']=form.errors
        return HttpResponse(json.dumps(result))

def register(request):
    """
    注册
    :param request:
    :return:
    """
    if request.method=="GET":
        return render(request, 'register.html')
    elif request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        print(username,password,email)
        new_user = models.UserInfo.objects.create(username=username,password=password,email=email)
    return HttpResponse('注册成功')



def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.clear()
    return redirect('/login.html')

