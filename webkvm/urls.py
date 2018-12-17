from django.urls import path, re_path
from django.conf import settings

from servers import views
from django.contrib.auth import views as dviews
from hostdetail import views as hviews
from create import v

urlpatterns = ['',
               path(r'^$', views.index, name="index"),
               path(r'^login/$', dviews.auth_login, {'templae_name': 'login.html'}, name='login'),
               path(r'^logout/$', dviews.auth_logout, {'templae_name': 'logout.html'}, name='logout'),
               path(r'^servers/$', views.servers_list, name='servers_list'),
               path(r'^infrastructure/$', views.infrastructure, name='infrastructure'),
               path(r'^host/(\d+)/$',hviews.overview,name='overview'),
               path(r'^create/(\d+)',)
               ]
