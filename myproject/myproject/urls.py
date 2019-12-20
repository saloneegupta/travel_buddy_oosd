"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from cabshare import views
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.view_cabs, name='home'),
    url(r'^view_cabs/$', views.view_cabs, name='view_cabs'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^approve_cab/(?P<pk_cab>[\w.@+-]+)/for_user/(?P<pk_user>[\w.@+-]+)/$', views.approve_cab, name='approve_cab'),
    url(r'^decline_cab/(?P<pk_cab>[\w.@+-]+)/for_user/(?P<pk_user>[\w.@+-]+)/$', views.decline_cab, name='decline_cab'),
    url(r'^contact_details/(?P<pk>\d+)/$', views.contact_details, name='contact_details'),
    url(r'^not_authorized/$', views.contact_details, name='not_authorized'),

    url(r'^user_info_for_new_cab/$', views.user_info_for_new_cab, name='user_info_for_new_cab'),
    url(r'^user_info_for_user_details/$', views.user_info_for_user_details, name='user_info_for_user_details'),
    url(r'^user_info_for_admin_panel/$', views.user_info_for_admin_panel, name='user_info_for_admin_panel'),
    url(r'^user_info_for_request_cab/(?P<pk>\d+)/$', views.user_info_for_request_cab, name='user_info_for_request_cab'),
    url(r'^cab_info/(?P<pk>\d+)/$', views.cab_info, name='cab_info'),
    url(r'^(?P<username>[\w.@+-]+)/new_cab/$', views.new_cab, name='new_cab'),
    url(r'^(?P<username>[\w.@+-]+)/user_details/$', views.user_details, name='user_details'),
    url(r'^(?P<username>[\w.@+-]+)/cab_admin_panel/$', views.cab_admin_panel, name='cab_admin_panel'),
    url(r'^(?P<username>[\w.@+-]+)/manage_cab/(?P<pk>\d+)/$', views.manage_cab, name='manage_cab'), 
    url(r'^admin/', admin.site.urls),
]
