from django.contrib import admin
from  .models import BlogType,Blog
# Register your models here.

class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ['id','type_name']

admin.site.register(BlogType,BlogTypeAdmin)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','blog_type','author','get_read_num','created_time','last_updated_time']
    list_per_page = 10
admin.site.register(Blog,BlogAdmin)
'''
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['read_num','blog']
admin.site.register(ReadNum,ReadNumAdmin)'''