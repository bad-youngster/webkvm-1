from django.conf.urls import url,include

from django.views.generic import TemplateView

from servers.views import servers_list,infrastructure,index


urlpatterns = [
    url(r'^$', index, name='index'),
    # url(r'^login/', TemplateView.as_view(template_name= "login.html"),
    #         name='login'),
    url(r'^login/', TemplateView.as_view(template_name="login.html"),name='login'),
    url(r'^logout/', TemplateView.as_view(template_name="logout.html"),
        name='logout'),
    url(r'^servers/', servers_list, name='servers_list'),
    url(r'^infrastructure/', infrastructure, name='infrastructure'),
    # url('^host/', overview, name='overview'),
    # url(r'^create/$', include(create),name='creata'),
    # url('^storages/', storages, name='storages'),
    # url('^storage/', storage, name='storage'),
    # url('^networks/', networks, name='networks'),
    # url('^network/', network, name='network'),
    # url('^interfaces/', interfaces, name='interfaces'),
    # url('^interface/', interface, name='interface'),
    # url('^instances/', instances, name='instances'),
    # url('^instance/', instance, name='instance'),
    # url('^secrets/', include(secrets), name='secrets'),
    # url('^console/', console, name='console'),
    # url('^info/hostusage/', hostusage, name='hostusage'),
    # url('^info/insts_status/', insts_status, name='insts_status'),
    # url('^info/inst_status/', inst_status, name='inst_status'),
    # url('^info/instusage/', instusage, name='instusage'),

]
