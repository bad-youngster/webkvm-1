import random
from xml import etree

import libxml2

import libvirt
import lxml

def get_kvm_available(xml):
    kvm_domains = get_xml_path(xml,"//domain/@type='kvm'")


def randomMAC():
    #qemu mac

    oul = [0x52, 0x54, 0x00]

    mac = oul + [random.randint(0x00,0xff),
                 random.randint(0x00,0xff),
                 random.randint(0x00,0xff),
                 ]
    return ':'.join(map(lambda x: "%02x" % x,mac))


def randomUUID():

    #create  kvm  uuid      aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee
    uuid = [random.randint(0,255) for dummy in range(0,16)]

    return "-".join(["%02x" * 4,"%02x" * 2,"%02x" * 2,"%02x" * 2,"%02x" * 6]) % tuple(uuid)

def get_max_vcpus(conn,type=None):
    # libvirt pool for max possible vcpus

    if type is None:
        type = conn.getType()
    try:
        max = conn.getMaxVcpus(type.lower())
    except libvirt.libvirtError:
        max = 32
    return max

def xml_escape(str):

    if str in None:

        return None

    str = str.replace("&","&amp;")
    str = str.replace("'", "&apos;")
    str = str.replace("\"", "&quot;")
    str = str.replace("<", "&lt;")
    str = str.replace(">", "&gt;")
    return str

def compareMAC(p,q):
    #diff two mac addresses

    paddress = p.split(":")
    qaddress = q.split(":")

    if len(paddress) != len(qaddress):

        if p < q:
            return 1
        else:
            return -1

    for i in range(len(paddress)):
        n = int(paddress[i],0x10) - int(qaddress[i],0x10)

        if n > 0:
            return 1
        elif n < 0:
            return -1
    return 0
def get_xml_path(xml,path=None,func=None):

    # return the content from the passed xml xpath

    doc = None
    ctx = None
    result = None

    try:
        doc = libxml2.parseDoc(xml)
        ctx = doc.xpathNewContext()

        if path:
            ret = ctx.xpathEval(path)

            if ret is not None:
                if type (ret) == list:
                    if len(ret) >= 1:
                        result = ret[0].content
                    else:
                        result = ret


        elif func:
            result = func(ctx)
        else:
            raise ValueError("'path' or 'func' is required")
    finally:
        if doc:
            doc.freeDoc()
        if ctx:
            ctx.xpathFreeContext()
    return result

def pretty_mem(val):
    val = int(val)

    #changger unit   KB --> MB --> GB
    if val > (10 * 1024 * 1024):
        return "%2.2f GB" % (val / (1024.0 * 1024.0))
    else:
        return "%2.2f MB" % (val / 1024.0)

def pretty_bytes(val):
    val = int(val)

    # changger unit   KB --> MB --> GB
    if val > (1024 * 1024 * 1024):
        return "%2.2f GB" % (val / (1024.0 * 1024.0 * 1024.0))
    else:
        return "%2.2f MB" % (val / 1024.0 * 1024.0)


