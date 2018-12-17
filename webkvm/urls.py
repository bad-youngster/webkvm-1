from django.urls import path, re_path
from django.conf import settings

from servers import views as sviews
from django.contrib.auth import views as dviews
from hostdetail import views as hviews
from create import views as cviews
from storages import views as tviews
from networks import views as nviews
from interfaces import views as iviews
from instance import views as inviews

urlpatterns = ['',
               path(r'^$', sviews.index, name="index"),
               path(r'^login/$', dviews.auth_login, {'templae_name': 'login.html'}, name='login'),
               path(r'^logout/$', dviews.auth_logout, {'templae_name': 'logout.html'}, name='logout'),
               path(r'^servers/$', sviews.servers_list, name='servers_list'),
               path(r'^infrastructure/$', sviews.infrastructure, name='infrastructure'),
               path(r'^host/(\d+)/$',hviews.overview,name='overview'),
               path(r'^create/(\d+)',cviews.create,name='create'),
               path(r'^storages/(\d+)/$',tviews.storages,name='storages'),
               path(r'^storage/(\d+)/[\w\-\.]+)/$',tviews.storage,name='storage'),
               path(r'^networks/(\d+)/$', nviews.networks, name='networks'),
               path(r'^network/(\d+)/[\w\-\.]+)/$', nviews.network, name='network'),
               path(r'^interfaces/(\d+)/$', iviews.interfaces, name='interfaces'),
               path(r'^interface/(\d+)/[\w\.\:]+)/$', iviews.interface, name='interface'),
               path(r'^instances/(\d+)/$', iviews.interfaces, name='instances'),
               path(r'^instance/(\d+)/[\w\-\.\_]+)/$', iviews.interface, name='instance'),
               ]
