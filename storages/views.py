from django.http import HttpResponseRedirect
from django.urls import reverse


def storages(request,host_id):
    # storage pool

    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    errors = []
    compute = abs()