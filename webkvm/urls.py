from django.contrib.auth import login, logout
from django.urls import path, re_path
from django.conf import settings

from hostdetail.views import overview, hostusage
from instance.views import instances, instance, insts_status, inst_status, instusage
from interfaces.views import interfaces, interface
from networks.views import networks, network
from servers.views import index,servers_list,infrastructure
from storages.views import storages, storage
from vrtkvm import create, secrets

urlpatterns = ['',
               # path(r'^$', 'servers.views.index', name="index"),
               path(r'^$', index,name='index'),
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

               path(r'^login/$', login, {'templae_name': 'login.html'},
                    name='login'),
               path(r'^logout/$', logout, {'templae_name': 'logout.html'},
                    name='logout'),
               path(r'^servers/$', servers_list, name='servers_list'),
               path(r'^infrastructure/$', infrastructure, name='infrastructure'),
               path(r'^host/(\d+)/$', overview, name='overview'),
               path(r'^create/(\d+)', create, name='create'),
               path(r'^storages/(\d+)/$', storages, name='storages'),
               path(r'^storage/(\d+)/[\w\-\.]+)/$', storage, name='storage'),
               path(r'^networks/(\d+)/$', networks, name='networks'),
               path(r'^network/(\d+)/[\w\-\.]+)/$', network, name='network'),
               path(r'^interfaces/(\d+)/$', interfaces, name='interfaces'),
               path(r'^interface/(\d+)/[\w\.\:]+)/$', interface, name='interface'),
               path(r'^instances/(\d+)/$', instances, name='instances'),
               path(r'^instance/(\d+)/[\w\-\.\_]+)/$', instance, name='instance'),
               path(r'^secrets/(\d+)/$', secrets, name='secrets'),
               path(r'^console/$', 'console.views.console', name='console'),
               path(r'^info/hostusage/(\d+)/$', hostusage, name='hostusage'),
               path(r'^info/insts_status/(\d+)/$', insts_status, name='insts_status'),
               path(r'^info/inst_status/(\d+)/([\w\-\.]+)/$', inst_status, name='inst_status'),
               path(r'^info/instusage/(\d+)/([\w\-\.]+)/$', instusage, name='instusage'),
]