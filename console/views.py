import re

from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.urls import reverse

from instance.models import Instance
from vrtkvm.instance import WvmInstance

from webkvm.settings import WS_PORT
from webkvm.settings import WS_PUBLIC_HOST


def console(request):
    """
    Console instance block
    """
    global token
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    if request.method == 'GET':
        token = request.GET.get('token', '')

    try:
        temptoken = token.split('-', 1)
        host = int(temptoken[0])
        uuid = temptoken[1]
        instance = Instance.objects.get(compute_id=host, uuid=uuid)
        conn = WvmInstance(instance.compute.hostname,
                           instance.compute.login,
                           instance.compute.password,
                           instance.compute.type,
                           instance.name)
        console_type = conn.get_console_type()
        console_websocket_port = conn.get_console_websocket_port()
        console_passwd = conn.get_console_passwd()
    except:
        console_type = None
        console_websocket_port = None
        console_passwd = None

    ws_port = console_websocket_port if console_websocket_port else WS_PORT
    ws_host = WS_PUBLIC_HOST if WS_PUBLIC_HOST else request.get_host()

    if ':' in ws_host:
        ws_host = re.sub(':[0-9]+', '', ws_host)

    if console_type == 'vnc':
        response = render(request,'console-vnc.html', locals())
    elif console_type == 'spice':
        response = render(request,'console-spice.html', locals())
    else:
        response = "Console type %s no support" % console_type

    response.set_cookie('token', token)
    return response
