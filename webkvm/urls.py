from django.urls import path, re_path
from django.conf import settings


urlpatterns = ['',
               path(r'^$', 'servers.views.index', name="index"),
               path(r'^login/$', 'django.contrib.auth.views.auth_login', {'templae_name': 'login.html'}, name='login'),
               path(r'^logout/$', 'django.contrib.auth.views.auth_logout', {'templae_name': 'logout.html'}, name='logout'),
               path(r'^servers/$', 'servers.views.servers_list', name='servers_list'),
               path(r'^infrastructure/$', 'servers.views.infrastructure', name='infrastructure'),
               path(r'^host/(\d+)/$','hostdetail.views.overview',name='overview'),
               path(r'^create/(\d+)','create.views.create',name='create'),
               path(r'^storages/(\d+)/$','storages.views.storages',name='storages'),
               path(r'^storage/(\d+)/[\w\-\.]+)/$','storages.views.storage',name='storage'),
               path(r'^networks/(\d+)/$', 'networks.views.networks', name='networks'),
               path(r'^network/(\d+)/[\w\-\.]+)/$', 'networks.views.network', name='network'),
               path(r'^interfaces/(\d+)/$', 'interfaces.views.interfaces', name='interfaces'),
               path(r'^interface/(\d+)/[\w\.\:]+)/$', 'interfaces.views.interface', name='interface'),
               path(r'^instances/(\d+)/$', 'instance.views.instances', name='instances'),
               path(r'^instance/(\d+)/[\w\-\.\_]+)/$', 'instance.views.instance', name='instance'),
               path(r'^secrets/(\d+)/$', 'secrets.views.secrets', name='secrets'),
               path(r'^console/$', 'console.views.console', name='console'),
               path(r'^info/hostusage/(\d+)/$', 'hostdetail.views.hostusage', name='hostusage'),
               path(r'^info/insts_status/(\d+)/$', 'instance.views.insts_status', name='insts_status'),
               path(r'^info/inst_status/(\d+)/([\w\-\.]+)/$', 'instance.views.inst_status', name='inst_status'),
               path(r'^info/instusage/(\d+)/([\w\-\.]+)/$', 'instance.views.instusage', name='instusage'),



               ]
