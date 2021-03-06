from django.shortcuts import render
from django.shortcuts import render_to_response,get_object_or_404#可能还会娶不到
from read_statistics.utils import get_seven_days_read_data
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
def home(request):
    blog_content_type=ContentType.objects.get_for_model(Blog)
    dates, read_nums= get_seven_days_read_data(blog_content_type)
    context={}
    context['dates']=dates
    context['read_nums']=read_nums
    return render(request,'home.html',context)
def error(request):
    context={}
    return render_to_response('error.html',context)


