from django.db import models
from django.db.models.fields import exceptions#异常处理
from django.utils import timezone
# Create your models here.
#怎么去关联别的模型呢
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
class ReadNum(models.Model):
    read_num=models.IntegerField(default=0)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)#指向那个ContentType模型
    object_id=models.PositiveIntegerField()#数值类型
    content_object=GenericForeignKey('content_type','object_id')

class ReadNumExpandMethod():#拓展方法
    def get_read_num(self):
         try:
            ct = ContentType.objects.get_for_model(self)  # 获取模型
            readnum= ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
         except exceptions.ObjectDoesNotExist:
             return 0
class ReadDetail(models.Model):#记录详细的阅读计数
    date=models.DateField(default=timezone.now)#获取某天
    read_num=models.IntegerField(default=0)

    content_type=models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')