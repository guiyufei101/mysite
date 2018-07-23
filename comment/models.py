from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
#关联任何类型
# Create your models here.
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 指向那个ContentType模型
    object_id = models.PositiveIntegerField()  # 数值类型
    content_object = GenericForeignKey('content_type', 'object_id')
    #评论对象创建好了不光是blog

    text=models.TextField()#评论内容
    comment_time=models.DateTimeField(auto_now_add=True)#评论时间
    user=models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)#评论者关联用户

    #parent_id=models.IntegerField(default=0)#关联它的上一级，就知道回复的是哪一条
    root=models.ForeignKey('self',related_name="root_comment",null=True,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',related_name="parent_comment",null=True,on_delete=models.CASCADE)#指向自己,第一层为空它没有上一级
    reply_to=models.ForeignKey(User,related_name="replies",null=True,on_delete=models.CASCADE)#回复谁的外键不能同时两个指向一个

    def __str__(self):
        return self.text
    class Meta:#排序
        ordering=['comment_time']



#回复可以是无限的这样就得想一种比较合理的做法，把回复当成评论，回复本质就是评论
