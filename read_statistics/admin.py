from django.contrib import admin
from .models import ReadNum,ReadDetail
# Register your models here.
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ['read_num','content_object']
admin.site.register(ReadNum,ReadNumAdmin)

class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ['date','read_num','content_object']
admin.site.register(ReadDetail,ReadDetailAdmin)