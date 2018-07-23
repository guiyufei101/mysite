from django.db import models
from django.contrib.auth.models import User
#引入ckeditor
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import exceptions#异常处理
from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum
from read_statistics.models import ReadNumExpandMethod#拓展的方法
from django.shortcuts import reverse#逆向域名
# Create your models here.

"""class test():
    def get_read_num(self):
         ct=ContentType.objects.get_for_model(Blog)#获取模型
         try:

            readnum=ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return readnum.read_num
         except exceptions.ObjectDoesNotExist:
             return 0"""

class BlogType(models.Model):
    type_name=models.CharField(max_length=15)
    def __str__(self):#显示字符内容 否则在别的模型中看到是串
        return  self.type_name

#class Blog(models.Model,test):#还继承了test这个
class Blog(models.Model,ReadNumExpandMethod):
    title=models.CharField(max_length=50)
    blog_type=models.ForeignKey(BlogType,on_delete=models.DO_NOTHING,related_name='blog_blog')
    #content=models.TextField()
    #content=RichTextField()#替换掉上面的内容是不允许上传文件的
    content=RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    #read_num=models.IntegerField(default=0)#计数默认是0

    created_time=models.DateTimeField(auto_now_add=True)
    last_updated_time=models.DateTimeField(auto_now=True)
    '''#返回计数值
    def get_read_num(self):
        #如果没有这个记录取捕获这个错误
        try:
            return self.readnum.read_num#返回对应对象的计数值
        except exceptions.ObjectDoesNotExist:#不存在返回0
            return 0'''

    def __str__(self):
        return "<Blog: %s>" % self.title
    class Meta:#排序操作
        ordering=['-created_time']#倒序排列
    def get_url(self):
        return reverse('blog_detail',kwargs={'blog_pk': self.pk})
    def get_email(self):
        return self.author.email
'''
class ReadNum(models.Model):
    read_num=models.IntegerField(default=0)
    blog=models.OneToOneField(Blog,on_delete=models.DO_NOTHING)'''
