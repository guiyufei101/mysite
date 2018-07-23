from django.contrib.contenttypes.models import ContentType
from read_statistics.models import ReadNum,ReadDetail
from django.utils import timezone
import datetime
from django.db.models import Sum
def read_statistics_once_read(request, obj):#obj为传过来的对象
    ct = ContentType.objects.get_for_model(obj)
    key ="%s_%s_read" % (ct.model, obj.pk)
    if not request.COOKIES.get(key):
        if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
            #存在这个记录
            readnum=ReadNum.objects.get(content_type=ct,object_id=obj.pk)
            readnum.read_num += 1
            readnum.save()
        else:
            #不存在记录
            readnum=ReadNum(content_type=ct,object_id=obj.pk)
            readnum.read_num += 1
            readnum.save()
        #明细加1
        time = timezone.now().date()
        if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk,date=time).count():#判断是否有记录
            readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk,date=time)
        else:
            readDetail=ReadDetail(content_type=ct, object_id=obj.pk,date=time)#实例化
        readDetail.read_num += 1
        readDetail.save()
        return key
def get_seven_days_read_data(content_type):
    today=timezone.now().date()#获取当前日期
    yesterday=today - datetime.timedelta(days=1)
    read_nums=[]
    dates=[]
    for  i in range(7, 0,-1):
        date=today-datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details=ReadDetail.objects.filter(content_type=content_type,date=date)#加总聚合
        result=read_details.aggregate(read_num_sum=Sum('read_num'))#求和
        read_nums.append(result['read_num_sum'] or 0)#对于每个数据加进去
    return dates,read_nums#返回出数据