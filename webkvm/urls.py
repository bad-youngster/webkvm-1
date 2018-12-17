from django.urls import path, re_path
from django.conf import settings

from servers import views as sviews
from django.contrib.auth import views as dviews
from hostdetail import views as hviews
from create import views as cviews
from storages import views as tviews

urlpatterns = ['',
               path(r'^$', sviews.index, name="index"),
               path(r'^login/$', dviews.auth_login, {'templae_name': 'login.html'}, name='login'),
               path(r'^logout/$', dviews.auth_logout, {'templae_name': 'logout.html'}, name='logout'),
               path(r'^servers/$', sviews.servers_list, name='servers_list'),
               path(r'^infrastructure/$', sviews.infrastructure, name='infrastructure'),
               path(r'^host/(\d+)/$',hviews.overview,name='overview'),
               path(r'^create/(\d+)',cviews.create,name='create'),
               path(r'^storages/(\d+)/$',tviews.storages,name='storages'),
               path(r'^storage/(\d+)/[\w\-\.]+)/$',tviews.storage,name='storages'),

               ]
