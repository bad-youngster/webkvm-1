from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from libvirt import libvirtError

from instance.models import Instance
from servers.forms import ComputeAddTcpForm,ComputeAddSshForm,ComputeAddTlsForm,ComputeEditHostForm
from servers.models import Compute
from vrtkvm.connection import connection_manager, CONN_TCP, CONN_SSH, CONN_TLS, CONN_SOCKET
from vrtkvm.hostdetails import WvmHostDetails


def index(request):
    #index page

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reversed('login'))
    else:
        return HttpResponseRedirect(reversed('servers_list'))

def servers_list(request):
    #server page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reversed('login'))

    def get_hosts_status(hosts):
        # get all hosts all vds on host
        all_hosts = []
        for host in hosts:
            all_hosts.append({
                'id': host.id,
                'name': host.name,
                'hostname': host.hostname,
                'status': connection_manager.host_is_up(host.type,host.hostname),
                'type': host.type,
                'login': host.login,
                'password': host.password,
            })
        return  all_hosts

    computes = Compute.objects.filter()
    hosts_info = get_hosts_status(computes)
    form = None

    if request.method == 'POST':
        if 'host_del' in request.POST:
            compute_id = request.POST.get('host_id', '')
            try:
                del_inst_on_host = Instance.objects.filter(compute_id=compute_id)
                del_inst_on_host.delete()
            finally:
                del_host = Compute.objects.get(id=compute_id)
                del_host.delete()

            return HttpResponseRedirect(request.get_full_path())
        if 'host_tcp_add' in request.POST:
            form = ComputeAddTcpForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_tcp_host = Compute(name=data['name'],
                                       hostname=data['hostname'],
                                       type=CONN_TCP,
                                       login=data['login'],
                                       password=data['password'])
                new_tcp_host.save()
                return HttpResponseRedirect(request.get_full_path())

        if 'host_ssh_add' in request.POST:
            form = ComputeAddSshForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_ssh_host = Compute(name=data['name'],
                                       hostname=data['hostname'],
                                       type=CONN_SSH,
                                       login=data['login'],
                                       )
                new_ssh_host.save()
                return HttpResponseRedirect(request.get_full_path())

        if 'host_tls_add' in request.POST:
            form = ComputeAddTlsForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_tls_host = Compute(name=data['name'],
                                       hostname=data['hostname'],
                                       type=CONN_TLS,
                                       login=data['login'],
                                       )
                new_tls_host.save()
                return HttpResponseRedirect(request.get_full_path())

        if 'host_edit' in request.POST:
            form = ComputeEditHostForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                compute_edit = Compute.objects.get(id=data['host_id'])
                compute_edit.name = data['name']
                compute_edit.hostname = data['hostname']
                compute_edit.login = data['login']
                compute_edit.password = data['password']
                compute_edit.save()
                return HttpResponseRedirect(request.get_full_path())

        if 'host_socket_add' in request.POST:
            form = ComputeAddTlsForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                new_socket_host = Compute(name=data['name'],
                                          hostname='localhost',
                                          type=CONN_SOCKET,
                                          login='',
                                          password='', )
                new_socket_host.save()
                return HttpResponseRedirect(request.get_full_path())
    return  render_to_response('servers.html', locals())

def infrastructure(request):
    # infrastructure page.

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reversed('login'))
    compute = Compute.objects.filter()
    hosts_vms = {}

    for host in compute:
        status = connection_manager.host_is_up(host.type,host.hostname)
        if status:
            try:
                conn = WvmHostDetails(host,host.login,host.password,host.type)
                host_info = conn.get_node_info()
                host_mem = conn.get_memory_usage()
                hosts_vms[host.id,host.name,status,host_info[3],host_info[2],
                          host_mem['percent']] = conn.get_host_instances()

                conn.close()
            except libvirtError:
                hosts_vms[host.id,host.name,status,0,0,0] = None
        else:
            hosts_vms[host.id,host.name,2,0,0,0] = None
    return render(request,'infrastructure.html', locals())

