from django.shortcuts import render
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from .forms import CommentForm
from django.http import JsonResponse
from django.core.mail import send_mail
from django.shortcuts import reverse#逆向域名
from django.conf import settings
# Create your views here.

#创建提交评论方法
def update_comment(request):
    '''referer = request.META.get('HTTP_REFERER', '')
    user=request.user

    #数据检查
    if not user.is_authenticated:
        return render(request, 'error.html', {'message': '用户未登录','redirect_to':referer})
    text=request.POST.get('text','').strip()#后面这个为去掉空格
    if text =='':
        return render(request,'error.html',{'message':'评论内容为空','redirect_to':referer})
    try:
        content_type=request.POST.get('content_type','')
        object_id=int(request.POST.get('object_id',''))
        #得到模型的具体类型
        model_class=ContentType.objects.get(model=content_type).model_class()
        model_obj=model_class.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message': '评论对象不存在','redirect_to':referer})

    #检查通过，保存数据
    comment=Comment()
    comment.user=user
    comment.text=text
    comment.content_object=model_obj#评论对象
    comment.save()

    return redirect(referer)#重定向'''
    referer = request.META.get('HTTP_REFERER', '')
    #if not request.user.is_authenticated:#用户未登录
        #return render(request,'error.html',{'message':'用户未登录','redirect_to':referer})
    comment_form=CommentForm(request.POST,user=request.user)
    if comment_form.is_valid():
        comment=Comment()
        comment.user=comment_form.cleaned_data['user']
        comment.text=comment_form.cleaned_data['text']#获取text内容
        comment.content_object=comment_form.cleaned_data['content_object']

        parent= comment_form.cleaned_data['parent']#取出parent
        if not parent is None:
            comment.root=parent.root if not parent.root is None else parent
            comment.parent=parent
            comment.reply_to=parent.user
        comment.save()
        #发送邮件通知
        if comment.parent is None:
            #评论我的博客
            # 发送邮件
            subject='有人评论你的博客'
            text= comment.text + '\n' + comment.content_object.get_url()
            email=comment.content_object.get_email()
            #email='1963119101@qq.com'
            if email !='':
                send_mail(
                    subject,
                    text,
                    '1963119101@qq.com',
                    [email],
                    fail_silently=False,
                )
        else:
            #回复我的评论
            subject = '有人回复你的评论'
            text = comment.text + '\n' + comment.content_object.get_url()
            email = comment.reply_to.email
            if email !='':
                send_mail(
                    subject,
                    text,
                    '1963119101@qq.com',
                    [email],
                    fail_silently=False,
                )
        #返回数据
        #return redirect(referer)
        data={}
        data['status']='SUCCESS'
        data['username']=comment.user.username
        #data['comment_time']=comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_time']=comment.comment_time.timestamp()
        data['text']=comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to']=comment.reply_to.username
        else:
            data['reply_to']=''
        data['pk']=comment.pk
        data['root_pk']=comment.root.pk if not comment.root is None else ''
        return JsonResponse(data)
    else:
        #return render(request, 'error.html', {'message':comment_form.errors, 'redirect_to': referer})
        data = {}
        data['status'] = 'ERROR'
        data['message']=list(comment_form.errors.values())[0][0]
        return JsonResponse(data)
