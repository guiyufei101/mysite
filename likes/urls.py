from django.urls import path
from . import views
#http://localhost:8000/blog/1

urlpatterns=[
    path('like_change/',views.like_change,name='like_change'),

]