from django.contrib.auth import login, logout
from django.urls import re_path
from django.conf import settings
from django.conf.urls import url,include

from console.views import console
from hostdetail.views import overview, hostusage
from instance.views import instances, instance, insts_status, inst_status, instusage
from interfaces.views import interfaces, interface
from networks.views import networks, network
from servers.views import index,servers_list,infrastructure
from storages.views import storages, storage
from vrtkvm import create, secrets

urlpatterns = ['',
               re_path('^$', index, name='index'),
               re_path('^login/', login, {'templae_name': 'login.html'},
                       name='login'),
               re_path('^logout/', logout, {'templae_name': 'logout.html'},
                       name='logout'),
               re_path('^servers/', servers_list, name='servers_list'),
               re_path('^infrastructure/', infrastructure, name='infrastructure'),
               re_path('^host/', overview, name='overview'),
               re_path('^create/', include(create)),
               re_path('^storages/', storages, name='storages'),
               re_path('^storage/', storage, name='storage'),
               re_path('^networks/', networks, name='networks'),
               re_path('^network/', network, name='network'),
               re_path('^interfaces/', interfaces, name='interfaces'),
               re_path('^interface/', interface, name='interface'),
               re_path('^instances/', instances, name='instances'),
               re_path('^instance/', instance, name='instance'),
               re_path('^secrets/', include(secrets), ),
               re_path('^console/', console, name='console'),
               re_path('^info/hostusage/', hostusage, name='hostusage'),
               re_path('^info/insts_status/', insts_status, name='insts_status'),
               re_path('^info/inst_status/', inst_status, name='inst_status'),
               re_path('^info/instusage/', instusage, name='instusage'),
               re_path('^aaa',instances),

               ]
