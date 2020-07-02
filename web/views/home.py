from django.shortcuts import HttpResponse,render,redirect
from repository import models
from django.urls import reverse
from utils.pagination import Pagination

def index(request,*args,**kwargs):
    """
    博客首页
    :param request:
    :return:
    """
    article_type_list = models.Article.type_choices
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        bass_url= reverse('index',kwargs=kwargs)
        print(bass_url)
    else:
        article_type_id=None
        bass_url='/'
    data_count = models.Article.objects.filter(**kwargs).count()
    if not data_count:
        data_count=1
    if article_type_id ==0:
        data_count = models.Article.objects.all().order_by('nid').count()
        page_obj = Pagination(request.GET.get('p'), data_count)
        article_list = models.Article.objects.all().order_by('nid')[page_obj.start:page_obj.end]
    else:
        page_obj = Pagination(request.GET.get('p'), data_count)
        article_list = models.Article.objects.filter(**kwargs).order_by('nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(bass_url)

    return render(
        request,
        'index.html',
        {
            'article_list':article_list,
            'article_type_list':article_type_list,
            'article_type_id':article_type_id,
            'page_str':page_str
        }
    )

def home(request,site):
    """
    个人首页
    :param request:
    :param site:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/all/0.html')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,date_format(creat_time,"%%Y-%%m") as ctime from repository_article group by date_format(creat_time,"%%Y-%%m")'
    )
    article_list = models.Article.objects.filter(blog=blog).order_by('nid').all()
    return render(
        request,
        'home.html',
        {
            'blog':blog,
            'tag_list':tag_list,
            'category_list':category_list,
            'date_list':date_list,
            'article_list':article_list
        }
    )

def filter(request,site,condition,val):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    if not blog:
        return redirect('/login')
    tag_list = models.Tag.objects.filter(blog=blog)
    category_list = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,date_format(creat_time,"%%Y-%%m") as ctime from repository_article group by date_format(creat_time,"%%Y-%%m")'
    )
    template_name = "home_summary_list.html"
    if condition =='tag':
        template_name='home_title_list.html'
        article_list = models.Article.objects.filter(tags=val,blog=blog).all()
    elif condition == 'category':
        article_list = models.Article.objects.filter(tags=val,blog=blog).all()
    elif condition == 'date':
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['date_format(creat_time,"%%Y-%%m")=%s'],params=[val,]).all()
    else:
        article_list=[]

    return render(
        request,
        template_name,
        {
            'blog':blog,
            'tag_list':tag_list,
            'category_list':category_list,
            'date_list':date_list,
            'article_list':article_list
        }
    )

def detail(request,site,nid):
    """
    博文详情
    :param request:
    :param site:
    :param nid:
    :return:
    """
    blog = models.Blog.objects.filter(site=site).select_related('user').first()
    tag_list = models.Tag.objects.filter(blog=blog)
    category = models.Category.objects.filter(blog=blog)
    date_list = models.Article.objects.raw(
        'select nid, count(nid) as num,date_format(creat_time,"%%Y-%%m") as ctime from repository_article group by date_format(creat_time,"%%Y-%%m")'
    )
    article = models.Article.objects.filter(blog=blog,nid=nid).select_related('category','articledetail').first()
    return render(
        request,
        'home_detail.html',
        {
            'blog':blog,
            'category':category,
            'date_list':date_list,
            'article':article
        }
    )