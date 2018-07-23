from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user =models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='昵称')
    nickname=models.CharField(max_length=20)

    def __str__(self):
        return '<Profile: %s for %s>' %(self.nickname,self.user.username)

def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''

def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username

def has_nickname(self):
    return Profile.objects.filter(user=self).exists()

User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname



class Userinfo(models.Model):
    user=models.OneToOneField(User,unique=True,on_delete=models.DO_NOTHING)
    tel=models.IntegerField(max_length=11,blank=True)
    photo=models.ImageField(blank=True)
    birthday=models.DateTimeField(blank=True)
    school=models.CharField(max_length=100,blank=True)
    company=models.CharField(max_length=100,blank=True)
    profession=models.CharField(max_length=100,blank=True)
    address=models.CharField(max_length=100,blank=True)

    def __str__(self):
        return "user:{}".format(self.user.username)
    def get_username(self):
        return self.user.username


