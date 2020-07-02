from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets
from django.core.exceptions import ValidationError
from repository import models
from .base import BaseForm

class LoginForm(BaseForm,django_forms.Form):
    username = django_fields.CharField(
        min_length=2,
        max_length=20,
        error_messages={'required':'用户名不能为空','min_length':'用户名过短','max_length':'用户名过长'}
    )
    password = django_fields.CharField(
        min_length=3,
        max_length=32,
        error_messages={'required': '密码不能为空.',
                        'invalid': '密码必须包含数字，字母、特殊字符',
                        'min_length': "密码长度不能小于8个字符",
                        'max_length': "密码长度不能大于32个字符"}
    )
    rmb = django_fields.IntegerField(required=False)

    check_code = django_fields.CharField(
        error_messages={'required':'验证码不能为空'}
    )
    def clean_check_code(self):
        if self.request.session.get('CheckCode').upper()!=self.request.POST.get('check_code').upper():
            raise ValidationError(message='验证码错误', code='invalid')
