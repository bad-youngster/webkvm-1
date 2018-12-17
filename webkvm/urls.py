from django.contrib.auth import login, logout
from django.urls import path, re_path
from django.conf import settings

from console.views import console
from hostdetail.views import overview, hostusage
from instance.views import instances, instance, insts_status, inst_status, instusage
from interfaces.views import interfaces, interface
from networks.views import networks, network
from servers.views import index,servers_list,infrastructure
from storages.views import storages, storage
from vrtkvm import create, secrets





urlpatterns = {'',
               # path(r'^$', 'servers.views.index', name="index"),
               re_path('^$', index, name='index'),
               # path(r'^login/$', 'django.contrib.auth.views.auth_login', {'templae_name': 'login.html'},
               #      name='login'),
               # path(r'^logout/$', 'django.contrib.auth.views.auth_logout', {'templae_name': 'logout.html'},
               #      name='logout'),
               # path(r'^servers/$', 'servers.views.servers_list', name='servers_list'),
               # path(r'^infrastructure/$', 'servers.views.infrastructure', name='infrastructure'),
               # path(r'^host/(\d+)/$','hostdetail.views.overview',name='overview'),
               # path(r'^create/(\d+)','create.views.create',name='create'),
               # path(r'^storages/(\d+)/$','storages.views.storages',name='storages'),
               # path(r'^storage/(\d+)/[\w\-\.]+)/$','storages.views.storage',name='storage'),
               # path(r'^networks/(\d+)/$', 'networks.views.networks', name='networks'),
               # path(r'^network/(\d+)/[\w\-\.]+)/$', 'networks.views.network', name='network'),
               # path(r'^interfaces/(\d+)/$', 'interfaces.views.interfaces', name='interfaces'),
               # path(r'^interface/(\d+)/[\w\.\:]+)/$', 'interfaces.views.interface', name='interface'),
               # path(r'^instances/(\d+)/$', 'instance.views.instances', name='instances'),
               # path(r'^instance/(\d+)/[\w\-\.\_]+)/$', 'instance.views.instance', name='instance'),
               # path(r'^secrets/(\d+)/$', 'secrets.views.secrets', name='secrets'),
               # path(r'^console/$', 'console.views.console', name='console'),
               # path(r'^info/hostusage/(\d+)/$', 'hostdetail.views.hostusage', name='hostusage'),
               # path(r'^info/insts_status/(\d+)/$', 'instance.views.insts_status', name='insts_status'),
               # path(r'^info/inst_status/(\d+)/([\w\-\.]+)/$', 'instance.views.inst_status', name='inst_status'),
               # path(r'^info/instusage/(\d+)/([\w\-\.]+)/$', 'instance.views.instusage', name='instusage'),

               re_path('^login/$', login, {'templae_name': 'login.html'},
                       name='login'),
               re_path('^logout/$', logout, {'templae_name': 'logout.html'},
                       name='logout'),
               re_path('^servers/$', servers_list, name='servers_list'),
               re_path('^infrastructure/$', infrastructure, name='infrastructure'),
               re_path('^host/(\d+)/$', overview, name='overview'),
               re_path('^create/(\d+)', create, name='create'),
               re_path('^storages/(\d+)/$', storages, name='storages'),
               re_path('^storage/(\d+)/[\w\-.]+)/$', storage, name='storage'),
               re_path('^networks/(\d+)/$', networks, name='networks'),
               re_path('^network/(\d+)/[\w\-.]+)/$', network, name='network'),
               re_path('^interfaces/(\d+)/$', interfaces, name='interfaces'),
               re_path('^interface/(\d+)/[\w.:]+)/$', interface, name='interface'),
               re_path('^instances/(\d+)/$', instances, name='instances'),
               re_path('^instance/(\d+)/[\w\-._]+)/$', instance, name='instance'),
               re_path('^secrets/(\d+)/$', secrets, name='secrets'),
               re_path('^console/$', console, name='console'),
               re_path('^info/hostusage/(\d+)/$', hostusage, name='hostusage'),
               re_path('^info/insts_status/(\d+)/$', insts_status, name='insts_status'),
               re_path('^info/inst_status/(\d+)/([\w\-.]+)/$', inst_status, name='inst_status'),
               re_path('^info/instusage/(\d+)/([\w\-.]+)/$', instusage, name='instusage'),
               }