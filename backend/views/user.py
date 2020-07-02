from ..auth.auth import check_login
from django.shortcuts import render,redirect,HttpResponse
from repository import models
import uuid
import os
import json
from django.http import JsonResponse
from utils.pagination import Pagination
from django.urls import reverse


@check_login
def index(request):
    print(request.session.get('user_info'))
    return render(request,'backend_index.html')

@check_login
def base_info(request):
    """
    个人信息
    :param request:
    :return:
    """
    current_username = request.session.get('user_info')
    email = models.UserInfo.objects.filter(username=current_username['username']).values('email','nickname')
    return render(request,'backend_base_info.html',{'current_username':current_username,'email':email})

@check_login
def upload_avatar(request):
    ret = {'status':False,'data':None,'message':None}
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar_img')
        if not file_obj:
            pass
        else:
            file_name = str(uuid.uuid4())
            file_path = os.path.join('static/imgs/avator',file_name)
            f = open(file_path,'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
            ret['status']=True
            ret['data']=file_path
    return HttpResponse(json.dumps(ret))

@check_login
def tag(request):
    """
    个人标签管理
    :param request:
    :return:
    """
    blog = models.Blog.objects.filter().select_related('user').first()

    if request.method == 'POST':
        tagname = request.POST.get('tagname')
    if not blog:
        return redirect('/login')
    tag_list = models.Tag.objects.filter(blog=blog).order_by('-nid')
    article_count = models.Article.objects.filter(blog=blog).count()
    return  render(request,'backend_tag.html',{'tag_list':tag_list,'article_count':article_count})

def del_tag(request):
    blog = models.Blog.objects.filter().select_related('user').first()
    if request.method == 'POST':
        tagname = request.POST.get('tagname')
        ds = request.POST.get('tag_id')
        mvtag = models.Tag.objects.filter(nid=ds).delete()
        response={'statu':True}
    return JsonResponse(response)

def add_tag(request):
    blog = models.Blog.objects.filter().select_related('user').first()
    if request.method == 'POST':
        tagname = request.POST.get('add_tag')
        if tagname =='':
            response = {'statu': False,'res':'请输入类型'}
        else:
            newtagname = models.Tag.objects.create(title=tagname, blog=blog)
            response={'statu':True}
    return JsonResponse(response)

def edit_tag(request):
    blog = models.Blog.objects.filter().select_related('user').first()
    tag_id = request.POST.get('tag_id')
    tag_title = request.POST.get('tag_title')
    tag_up = models.Tag.objects.filter(nid=tag_id).update(title=tag_title,blog=blog)
    res={'statu':True}
    return JsonResponse(res)

@check_login
def category(request,*args,**kwargs):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    bass_url = reverse('category', kwargs=kwargs)
    user=request.session.get('user_info')['blog__nid']
    if not user:
        return redirect('/login')
    date_count=models.Category.objects.filter(blog=user).count()
    page_obj=Pagination(request.GET.get('p'),date_count)
    from django.db.models.aggregates import Count
    date_list=models.Category.objects.filter(blog=user).annotate(c=Count('article__title')).values('title','c','nid')[page_obj.start:page_obj.end]
    # category_list = models.Category.objects.filter(blog=user)[page_obj.start:page_obj.end]
    # for i in category_list:
    #    article_sum=i.article_set.filter(blog=user).count()
    page_str = page_obj.page_str(bass_url)
    return  render(request,'backend_category.html',{'date_list':date_list,'page_str':page_str})

def add_category(request):
    blog = models.Blog.objects.filter().select_related('user').first()
    print(blog)
    add_cate = request.POST.get('add_cate')
    if add_cate =='':
        res = {'statu':False,'res':'请输入分类类型'}
    else:
        models.Category.objects.create(title=add_cate,blog=blog)
        res = {'statu':True}
    return JsonResponse(res)

def del_category(request):
    blog = models.Blog.objects.filter().select_related('user').first()
    del_cate_id = request.POST.get('cate_id')
    print(del_cate_id)
    try:
        models.Category.objects.filter(nid=del_cate_id).delete()
        res = {'statu':True}
    except Exception as err:
        res = {'statu':False,'res':'删除异常'}
    return JsonResponse(res)


@check_login
def article(request,*args,**kwargs):
    """
    个人文章管理
    :param request:
    :param args:
    :param kwargs:
    :return:
    """
    blog_id = request.session.get('user_info')
    # blog_id = request.session.get(['user_info']['blog__nid'])

    condition = {}
    for k,v in kwargs.items():
        kwargs[k] = int(v)
        if v == '0':
            pass
        else:
            condition[k] = v
    condition['blog_id']=blog_id['blog__nid']
    data_count = models.Article.objects.filter(**condition).count()
    page = Pagination(request.GET.get('p'),data_count)
    result = models.Article.objects.filter(**condition).order_by('-nid').only('nid','title','blog').select_related('blog')[page.start:page.end]
    page_str = page.page_str(reverse('article',kwargs=kwargs))
    category_list = models.Category.objects.filter(blog_id=blog_id['blog__nid']).values('nid','title')
    type_list = map(lambda item:{'nid':item[0],'title':item[1]},models.Article.type_choices)
    kwargs['p']=page.current_page
    return render(
        request,
        'backend_article.html',
        {
            'result':result,
            'page_str':page_str,
            'category_list':category_list,
            'type_list':type_list,
            'arg_dict':kwargs,
            'data_count':data_count
        }
    )