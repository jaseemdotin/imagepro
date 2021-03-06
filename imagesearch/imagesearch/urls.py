"""imagesearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homeView,name="home"),
    path('srch',views.samplesearch,name="search"),
    path('csvadd',views.csvAddView,name="csvadd"),
    path('imageadd',views.imageAddView,name="imageadd"),
    path('login',views.adminlogin,name="login"),
    path('logout',views.adminlogout,name="logout"),
    path('register',views.AdminRegister,name='register'),
    path('userlist',views.userlistview,name='userlist'),
    path('userlist/act/<int:id>',views.activateUserView,name='useractivate'),
    path('userlist/deact/<int:id>',views.deactivateUserView,name='userdeactivate'),
    path('imsample',views.samplesearch,name='sm'),
    path('userlist/edit/<int:id>',views.editUserView,name='edituser'),
    path('userlist/super/<int:id>',views.superUserView,name='superuser'),
]
