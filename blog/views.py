from django.shortcuts import render
from django.shortcuts import render_to_response,get_object_or_404#可能还会娶不到
from .models import BlogType,Blog
from django.core.paginator import Paginator#引入分页器
#方法2计数
from django.db.models import Count
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from comment.models import Comment
from read_statistics.utils import read_statistics_once_read#引入那个应用下的计数方法
from comment.forms import CommentForm
from user.forms import LoginForm
# Create your views here.

def blog_list(request):
    blogs_all_list=Blog.objects.all()
    paginator=Paginator(blogs_all_list,5)#每10个分一页
    page_num=request.GET.get('page',1)#获取url页面参数
    page_of_blogs=paginator.get_page(page_num)#对于字符串或者超过的页码会自动的识别为1
    #显示页码范围
    current_page_num=page_of_blogs.number#获取当前页码
    #将要显示的页码放到列表里返回给前端
    #page_range获取当前页前后两页的页码范围
    page_range=list(range(max(current_page_num -2,1),current_page_num))+list(range(current_page_num,min(current_page_num + 2 + 1,paginator.num_pages)))
    #需要判断第一页和最后一页paginator.num_pages
    #通过range方法得到。取-2和1的最大值,在python3里range()不是一个列表需要再加一个list
    # 加上省略页码标记
    if page_range[0] - 1 >=2:
        page_range.insert(0,'...')
    if paginator.num_pages - page_range[-1] >=2:
        page_range.append('...')
    if page_range[0] != 1:#把第一页加上
        page_range.insert(0,1)
    if page_range[-1] != paginator.num_pages:#把最后一页加上
        page_range.append(paginator.num_pages)
    context = {}
    #方法1 获取博客分类的对应博客数量
    """blog_types = BlogType.objects.all()
    blog_types_list = []  # 建一个列表将数量加到列表里
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)"""
    #方法2
    context['blog_types']=BlogType.objects.annotate(blog_count=Count('blog_blog'))

    #获取日期归档对应的博客数量
    blog_dates=Blog.objects.dates('created_time','month',order='DESC')
    blog_dates_dict={}
    for blog_date in blog_dates:#怎么放blog_count
        blog_count=Blog.objects.filter(created_time__year=blog_date.year,created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date]=blog_count
    blogs=Blog.objects.all()
    context['page_range']=page_range
    context['page_of_blogs']=page_of_blogs
    '''context['blog_types']=blog_types_list'''
    context['blogs_count']=Blog.objects.all().count()#统计总的博客数量
    context['blog_dates']=blog_dates_dict
    context['max_page']=paginator.num_pages
    return render(request,'blog_list.html',context)

def blog_detail(request,blog_pk):#blog_pk 为传过来的参数  可以写成id，blog_id
    blog=get_object_or_404(Blog,pk=blog_pk)#获取要访问的那个博客
    read_cookie_key=read_statistics_once_read(request,blog)
    blog_content_type=ContentType.objects.get_for_model(blog)
    #获取该博客所对应的所有评论
    comments=Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk,parent=None)#这是评论的
    #如果不存在这个访问记录时加1
    """if not request.COOKIES.get('blog_%s_read' % blog_pk):
        ct=ContentType.objects.get_for_model(Blog)
        if ReadNum.objects.filter(content_type=ct,object_id=blog.pk).count():
            #存在这个记录
            readnum=ReadNum.objects.get(content_type=ct,object_id=blog.pk)
            readnum.read_num+=1
            readnum.save()
        else:
            #不存在记录
            readnum=ReadNum(content_type=ct,object_id=blog.pk)
            readnum.read_num+=1
            readnum.save()

        #if  ReadNum.objects.filter(blog=blog).count():#存在这个记录
        #readnum=ReadNum.objects.get(blog=blog)#取出这个博客的计数记录
           #readnum.read_num+=1#计数加1
            #readnum.save()
        #else:
            #不存在记录
            #readnum=ReadNum()#创建记录
            #readnum.read_num +=1
            #readnum.blog=blog#对应
            #readnum.save()
        '''blog.read_num +=1#每次浏览加1
        blog.save()'''"""
    context = {}
    context['blog']=blog
    context['comments']=comments.order_by('-comment_time')
    #用filter得到查询集QuerySet
    #取比当前博客创建时间大的博客
    context['previous_blog']=Blog.objects.filter(created_time__gt=blog.created_time).last()#上一条博客
    context['next_blog']=Blog.objects.filter(created_time__lt=blog.created_time).first()#下一条博客
    context['user']=request.user
    context['login_form']=LoginForm()
    context['comment_count']=Comment.objects.filter(content_type=blog_content_type,object_id=blog.pk).count()#评论和回复计数
    data={}
    data['content_type']= blog_content_type.model
    data['object_id']= blog_pk
    data['reply_comment_id']=0
    context['comment_form']=CommentForm(initial=data)
    response = render(request,'blog_detail.html', context)#响应
    response.set_cookie('blog_%s_read' % blog_pk,'true',max_age=60)#将相关数据保存下来set_cookie(key,value,有效期)max_age=60秒有效,expires=datetime
    #response.set_cookie(read_cookie_key, 'true')#阅读cookie标记
    return response
def blogs_with_type(request,blog_type_pk):
    context={}
    #获取得到具体的类型
    blog_type=get_object_or_404(BlogType,pk=blog_type_pk)
    context['blog_type'] = blog_type
    blogs_all_list=Blog.objects.filter(blog_type=blog_type)

    paginator = Paginator(blogs_all_list, 5)  # 每10个分一页
    page_num = request.GET.get('page', 1)  # 获取url页面参数
    page_of_blogs = paginator.get_page(page_num)  # 对于字符串或者超过的页码会自动的识别为1
    # 显示页码范围
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 将要显示的页码放到列表里返回给前端
    # page_range获取当前页前后两页的页码范围
    if paginator.num_pages > 2:
        page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
            range(current_page_num, min(current_page_num + 2 + 1, paginator.num_pages)))
    else:
        page_range = page_of_blogs.paginator.page_range
    # 需要判断第一页和最后一页paginator.num_pages
    # 通过range方法得到。取-2和1的最大值,在python3里range()不是一个列表需要再加一个list
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:  # 把第一页加上
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:  # 把最后一页加上
        page_range.append(paginator.num_pages)

    #获取博客分类的对应博客数量
    blog_types=BlogType.objects.all()
    blog_types_list=[]#建一个列表将数量加到列表里
    for blog_type in blog_types:
        blog_type.blog_count=Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:  # 怎么放blog_count用字典实现
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                             created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    page_of_blogs = paginator.get_page(page_num)  # 对于字符串或者超过的页码会自动的识别为1
    context['page_of_blogs']=page_of_blogs
    context['page_range'] = page_range
    context['num']=blogs_all_list.count()
    context['blog_types'] = blog_types_list
    #context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    context['blog_dates']=blog_dates_dict
    return render(request,'blogs_with_type.html',context)

def blogs_with_date(request,year,month):
    context = {}

    blogs_all_list = Blog.objects.filter(created_time__year=year,created_time__month=month)
    paginator = Paginator(blogs_all_list, 5)  # 每10个分一页
    page_num = request.GET.get('page', 1)  # 获取url页面参数
    page_of_blogs = paginator.get_page(page_num)  # 对于字符串或者超过的页码会自动的识别为1
    # 显示页码范围
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 将要显示的页码放到列表里返回给前端
    # page_range获取当前页前后两页的页码范围
    if paginator.num_pages >2:
        page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
            range(current_page_num, min(current_page_num + 2 + 1, paginator.num_pages)))
    else:
        page_range=page_of_blogs.paginator.page_range
    # 需要判断第一页和最后一页paginator.num_pages
    # 通过range方法得到。取-2和1的最大值,在python3里range()不是一个列表需要再加一个list
    # 加上省略页码标记
    if paginator.num_pages > 2:
        if page_range[0] - 1 >= 2:
            page_range.insert(0, '...')
        if paginator.num_pages - page_range[-1] >= 2:
            page_range.append('...')
        if page_range[0] != 1:  # 把第一页加上
            page_range.insert(0, 1)
        if page_range[-1] != paginator.num_pages:  # 把最后一页加上
            page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    blog_types = BlogType.objects.all()
    blog_types_list = []  # 建一个列表将数量加到列表里
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:  # 怎么放blog_count用字典实现
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context['blogs']=page_of_blogs.object_list
    context['blogs_with_date']='%s年%s月' % (year,month)
    context['page_of_blogs']=page_of_blogs
    context['page_range']=page_range
    #context['blog_types']=BlogType.objects.all()
    context['blog_types']=blog_types_list
    context['blog_dates']=blog_dates_dict
    #context['blog_dates']=Blog.objects.dates('created_time','month',order="DESC")
    return render(request,'blogs_with_date.html',context)