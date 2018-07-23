from django.urls import path
from . import views
#http://localhost:8000/blog/1

urlpatterns=[
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),
    path('login/', views.login, name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logout,name='logout'),
    path('user_info/',views.user_info,name='user_info'),
    path('change_nickname/',views.change_nickname,name='change_nickname'),
    path('change_password/',views.change_password,name='change_password'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('imagecrop/', views.imagecrop, name='imagecrop'),
]