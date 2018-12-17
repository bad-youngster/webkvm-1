#coding:utf-8
import socket
import threading

import libvirt

from vrtkvm import util
from vrtkvm.rwlock import ReadWriteLock
from webkvm import settings

CONN_SOCKET = 4
CONN_TLS = 3
CONN_SSH = 2
CONN_TCP = 1
TLS_PORT = 16514
SSH_PORT = 22
TCP_PORT = 16509


class WvmEventLoop(threading.Thread):
    def __int__(self, group=None, target=None, name=None, args=(), kwargs=None):

        if kwargs is None:
            kwargs = {}

        libvirt.virEventRegisterDefaultImpl()

        if name is None:
            name = 'libvirt event loop'
        super(WvmEventLoop,self).__init__(group,target,name,args,kwargs)

        self.daemon = True

    def run(self):
        while True:

            libvirt.virEventRegisterDefaultImpl()

class WvmConnection(object):

    def __init__(self,host,login,passwd,conn):

        self.connection_state_lock = threading.Lock()
        self.connection = None
        self.last_error = None

        #connection host credentials
        self.host = host
        self.login = login
        self.passwd = passwd
        self.type = conn

    def connect(self):
        self.connection_state_lock.acquire()
        try:
            #recheck if we hava a connection
            if not self.connected:
                if self.type == CONN_TCP:
                    self.__connect_tcp()
                elif self.type == CONN_SSH:
                    self.__connect_ssh()
                elif self.type == CONN_TLS:
                    self.__connect_tls()
                elif self.type == CONN_SOCKET:
                    self.__connect_socket()
                else:
                    raise ValueError('"{type}" is not a valid connection type'.format(type=self.type))

                if self.connection:
                    # do set keep alive interval/set connection close/fail hander

                    try:
                        self.connection.setKeepAlive(connection_manager.keepalive_interval,connection_manager.keepalive_count)
                        try:
                            self.connection.registerCloseCallback(self.__connection_close_callback,None)

                        except:

                            pass
                    except libvirt.libvirtError as e:
                        self.last_error = str(e)
        finally:
            self.connection_state_lock.release()



    def connected(self):
        #recheck thread is runing or not runing
        try:
            return self.connection is not None and self.connection.isAlive()
        except libvirt.libvirtError:

            return False

    def __libvirt_auth_credentials_callback(self,credentials,user_data):
        #vir connect credential type
        for credential in credentials:
            #name credential type
            if credential[0] == libvirt.VIR_CRED_AUTHNAME:
                credential[4] = self.login
                if len(credential[4]) == 0:
                    credential[4] = credential[3]
            #passwd credential type
            elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
                credential[4] = self.passwd
            else:
                return -1
        return 0


    def __connection_close_callback(self,connection,reason,opaque=None):
        self.connection_state_lock.acquire()
        try:
            #kvm server shutdown libvirt module freed before the close are called check here if still present

            if libvirt is not None:
                if reason == libvirt.VIR_CONNECT_CLOSE_REASON_ERROR:
                    self.last_error = 'connection closed: Misc I/O error'
                elif (reason == libvirt.VIR_CONNECT_CLOSE_REASON_EOF):
                     self.last_error = 'connection closed: End-of-file from server'

                elif (reason == libvirt.VIR_CONNECT_CLOSE_REASON_KEEPALIVE):
                    self.last_error = 'connection closed: Keepalive timer triggered'

                elif (reason == libvirt.VIR_CONNECT_CLOSE_REASON_CLIENT):
                    self.last_error = 'connection closed: Client requested it'
                else:
                    self.last_error = 'connection closed: Unknown error'

                # prevent other threads from using the connection (in the future)
                self.connection = None
        finally:
                self.connection_state_lock.release()

    def __connect_tcp(self):
        flags = [libvirt.VIR_CRED_AUTHNAME,libvirt.VIR_CRED_PASSPHRASE]
        auth = [flags,self.__libvirt_auth_credentials_callback,None]
        url = 'qemu+tcp://%s/system' % self.host

        try:
            self.connection = libvirt.openAuth(url,auth,0)
            self.last_error = None

        except libvirt.libvirtError as e:
            self.last_error = 'Connection Failed: ' + str(e)
            self.connection = None

    def __connect_ssh(self):
        url = 'qemu+ssh://%s@%s/system' % (self.login,self.host)

        try:
            self.connection = libvirt.open(url)
            self.last_error = None
        except libvirt.libvirtError as e:
            self.last_error = 'Connection Failed: ' + str(e) + ' --- ' + repr(libvirt.virGetLastError())
            self.connection = None

    def __connect_tls(self):

        flags = [libvirt.VIR_CRED_AUTHNAME,libvirt.VIR_CRED_PASSPHRASE]
        auth = [flags,self.__libvirt_auth_credentials_callback,None]
        url = 'qemu+tls://%s@%s/system' % (self.login,self.host)

        try:
            self.connection = libvirt.openAuth(url,auth,0)
            self.last_error = None

        except libvirt.libvirtError as e:
            self.last_error = 'Connection Failed' + str(e)
            self.connection = None

    def __connect_socket(self):

        url = 'qemu:///system'

        try:
            self.connection = libvirt.open(url)
            self.last_error = None

        except libvirt.libvirtError as e:
            self.last_error = 'Connection Failed: ' + str(e)
            self.connection =None

    def close(self):

        #close the connection

        self.connection_state_lock.acquire()

        try:
            if self.connected:
                #handle error timeout
                try:
                    self.connection.close()
                except libvirt.libvirtError:
                    pass
            self.connection = None
            self.last_error = None
        finally:
            self.connection_state_lock.release()

    def __del__(self):
        if self.connection is not None:

            try:
                self.connection.unregisterCloseCallback()

            except:
                pass
    def __str__(self):
        #select connection type
        if self.type == CONN_TCP:
            type_str = u'tcp'
        elif self.type == CONN_SSH:
            type_str = u'ssh'
        elif self.type == CONN_TLS:
            type_str = u'tls'
        else:
            type_str = u'invalid_type'

        return u'qemu+{type}://{user}@{host}/system'.format(type=type_str,user=self.login,host=self.host)
    def __repr__(self):
        return '<WvmConnection {connection_str}>'.format(connection_str=str(self))

class WvmConnectionManager(object):
    def __init__(self,keepalive_interval=5,keepalive_count=5):
        self.keepalive_interval = keepalive_interval
        self.keepalive_count = keepalive_count

        #connection dict maps hostname to a list of connection objects for this hostname,with diffent logins or auth methods

        self._connections = dict()
        self._connections_lock = ReadWriteLock()
        #start event loop to handle keepalive

        self._event_loop = WvmEventLoop()
        self._event_loop.start()
    def _search_connection(self,host,login,passwd,conn):

        # search connection dict for a connection if not exist return none
        self._connections_lock.acquireRead()
        try:
            if (host in self._connections):
                connections = self._connections[host]

                for connection in connections:
                    if (connection.login == login and connection.passwd == passwd and connection.type == connection):
                        return connection
        finally:
            self._connections_lock.release()

        return None
    def get_connection(self,host,login,passwd,conn):
        # force all string values to str

        host = str(host)
        login = str(login)
        passwd = str(passwd) if passwd is not None else None

        connection = self._search_connection(host,login,passwd,conn)

        if (connection is None):
            self._connections_lock.acquireWrite()

            try:
                # we have to search for the connection again after aquireing the write lock

                connection = self._search_connection(host,login,passwd,conn)
                if (connection is None):
                    # create a new connection if a matching connection does not already exist
                    connection = WvmConnection(host,login,passwd,conn)

                    if host in self._connections:
                        self._connections[host].append(connection)
                    else:
                        self._connections[host] = [connection]
            finally:
                self._connections_lock.release()

        elif not connection.connected:
            connection.connect()

        if connection.connected:

            return connection.connection
        else:

            raise libvirt.libvirtError(connection.last_error)

    def host_is_up(self,conn_type,hostname):
        # if given host is up and we connection using credentials

        try:
            socket_host = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            socket_host.settimeout(1)

            if conn_type == CONN_SSH:
                if ':' in hostname:
                    LIBVIRT_HOST,PORT = (hostname).split(":")
                    PORT = int(PORT)
                else:
                    PORT = SSH_PORT
                    LIBVIRT_HOST = hostname
                socket_host.connect((LIBVIRT_HOST,PORT))
            if conn_type == CONN_TCP:
                socket_host.connect((hostname,TCP_PORT))
            if conn_type == CONN_TLS:
                socket_host.connect((hostname,TLS_PORT))
            socket_host.close()
            return  True
        except Exception as err:
            return err
#connection keep time for 5
connection_manager = WvmConnectionManager(

    settings.LIBVIRT_KEEPALIVE_INTERVAL
    if hasattr(settings,'LIBVIRT_KEEPALIVE_INTERVAL')
    else 5,

    settings.LIBVIRT_KEEPALIVE_COUNT
    if hasattr(settings,'LIBVIRT_KEEPALIVE_COUNT')
    else 5
)

class WvmConnect(object):

    def __init__(self,host,login,passwd,conn):

        self.host = host
        self.login = login
        self.passwd = passwd
        self.conn = conn

        #GET CONNECTION FROM MANAGER

        self.wvm = connection_manager.get_connection(host,login,passwd,conn)

    def get_cap_xml(self):
        #return xml capabilities

        return self.wvm.getCapabilites()

    def get_kvm_supported(self):
        #return kvm capabilities

        return util.get_kvm_available(self.get_cap_xml())

    def get_storages(self):

        storages = []

        for pool in self.wvm.listStoragePools():
            storages.append(pool)

        for pool in self.wvm.listDefinedStoragePools():
            storages.append(pool)

        return storages

    def get_networks(self):
        virtnet = []
        for net in self.wvm.listNetworks():
            virtnet.append(net)
        for net in self.wvm.listDefinedNetworks():
            virtnet.append(net)
        return virtnet

    def get_ifaces(self):
        interface = []
        for inface in self.wvm.listInterfaces():
            interface.append(inface)
        for inface in self.wvm.listDefinedInterfaces():
            interface.append(inface)
        return interface

    def get_iface(self,name):
        return self.wvm.interfaceLookupByName(name)

    def get_secrets(self):
        return self.wvm.listSecrets()

    def get_secret(self,uuid):
        return self.wvm.secretLookByUUIDString(uuid)

    def get_storage(self,name):
        return self.wvm.storagePoolLookupByName(name)

    def get_volume_by_path(self,path):
        return self.wvm.storageVolLookupByPath(path)

    def get_network(self,net):
        return self.wvm.networkLookupByName(net)

    def get_instance(self,name):
        return self.wvm.lookupByName(name)

    def get_instances(self):
        instances = []
        for inst_id in self.wvm.listDomainsID():
            dom = self.wvm.lookupByID(int(inst_id))
            instances.append(dom.name())

        for name in self.wvm.listDefinedDomains():
            instances.append(name)
        return instances

    def get_snapshots(self):

        instance = []

        for snap_id in self.wvm.listDomainsID():
            dom = self.wvm.lookupByID(int(snap_id))
            if dom.snapshotNum(0) != 0:
                instance.append(dom.name())
        for name in self.wvm.listDefinedDomains():
            dom = self.wvm.lookupByName(name)
            if dom.snapshotNum(0) != 0:
                instance.append(dom.name())
        return instance

    def get_net_device(self):
        netdevice = []
        for dev in self.wvm.listAllDevices(0):
            xml = dev.XMLDesc(0)
            dev_type = util.get_xml_path(xml,'/device/capability/@type')
            if dev_type == 'net':
                netdevice.append(util.get_xml_path(xml,'/device/capability/interface'))
        return  netdevice

    def get_host_instances(self):
        vname = {}
        memory = self.wvm.getInfo()[1] * 1048576
        for name in self.get_instances():
            dom = self.get_instance(name)
            mem = util.get_xml_path(dom.XMLDesc(0),"/domain/currentMemory")
            mem = int(mem) * 1024
            mem_usage = (mem * 100) / memory
            cur_vcpu = util.get_xml_path(dom.XMLDesc(0),"/domain/vcpu/@current")
            if cur_vcpu:
                vcpu = cur_vcpu
            else:
                vcpu = util.get_xml_path(dom.XMLDesc(0),"domain/vcpu")
            vname[dom.name()] = (dom.info()[0],vcpu,mem,mem_usage)

        return vname
    def close(self):
        # do not close connection self.wvm.close()
        pass