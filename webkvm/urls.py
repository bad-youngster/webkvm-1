from django.contrib.auth import login, logout
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
               url('^$', index, name='index'),
               url('^login/', login, {'templae_name': 'login.html'},
                       name='login'),
               url('^logout/', logout, {'templae_name': 'logout.html'},
                       name='logout'),
               url('^servers/', servers_list, name='servers_list'),
               url('^infrastructure/', infrastructure, name='infrastructure'),
               url('^host/', overview, name='overview'),
               url('^create/', include(create),name='creata'),
               url('^storages/', storages, name='storages'),
               url('^storage/', storage, name='storage'),
               url('^networks/', networks, name='networks'),
               url('^network/', network, name='network'),
               url('^interfaces/', interfaces, name='interfaces'),
               url('^interface/', interface, name='interface'),
               url('^instances/', instances, name='instances'),
               url('^instance/', instance, name='instance'),
               url('^secrets/', include(secrets), name='secrets'),
               url('^console/', console, name='console'),
               url('^info/hostusage/', hostusage, name='hostusage'),
               url('^info/insts_status/', insts_status, name='insts_status'),
               url('^info/inst_status/', inst_status, name='inst_status'),
               url('^info/instusage/', instusage, name='instusage'),

               ]
