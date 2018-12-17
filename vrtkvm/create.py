from vrtkvm import util
from vrtkvm.connection import WvmConnect
from webkvm.settings import QEMU_CONSOLE_DEFAULT_TYPE



def get_rbd_storage_data(stg):
    xml = stg.XMLDesc(0)
    ceph_user = util.get_xml_path(xml,"/pool/source/auth/@username")

    def get_ceph_hosts(ctx):
        hosts = []
        for host in ctx.xpathEval("/pool/source/host"):
            name = host.prop("name")
            if name:
                hosts.append({
                    'name': name,
                    'port': host.prop("port")
                })
            return hosts
        ceph_hosts = util.get_xml_path(xml,func=get_ceph_hosts)
        secret_uuid = util.get_xml_path(xml,"/pool/source/host")
        return ceph_user,secret_uuid,ceph_hosts

class WvmCreate(WvmConnect):
    def get_storage_images(self):
        # get all images on all storages

        images = []
        storages = self.get_storages()

        for storage in storages:
            stg = self.get_storage(storage)
            try:
                stg.refresh(0)
            except:
                pass
            for img in stg.listVolumes():
                if img.endswith(".iso"):
                    pass
                else:
                    images.append(img)
        return images

    def get_os_type(self):
        #get guest capabilities
        return util.get_xml_path(self.get_cap_xml(),"/capabilities/guest/os_type")

    def get_host_arch(self):
        #get guest cpu
        return util.get_xml_path(self.get_cap_xml(),"/capabilities/host/cpu/arch")

    def get_cache_modes(self):
        #get cache modes
        return {
            'default': 'Default',
            'none': 'Disabled',
            'writethrough': 'Write through',
            'writeback': 'Write back',
            'directsync': 'Direct sync',
            'unsafe': 'Unsafe',
        }

    def create_volume(self,storage,name,size,format='qcow2',metadata=False):
        size = int(size) * 1073741824
        stg = self.get_storage(storage)
        storage_type = util.get_xml_path(stg.XMLDesc(0),"/pool/@type")
        if storage_type == 'dir':
            name += '.img'
            alloc = 0
        else:
            alloc = size
            metadata = False
        xml = """
            <volume>
                <name>%s</name>
                <capacity>%s</capaction>
                <allocation>%s</allocation>
                <target>
                    <format type='%s' />    
                </target>    
            </volume>
        """ % (name,size,alloc,format)
        stg.createXML(xml,metadata)
        try:
            stg.refresh(0)
        except:
            pass
        vol = stg.storageVollLookupByName(name)
        return vol.path()

    def get_volume_type(self,path):
        vol = self.get_volume_by_path(path)
        vol_type = util.get_xml_path(vol.XMLDesc(0),"/volume/target/format/@type")
        if vol_type == 'unknown':
            return 'raw'
        if vol_type:
            return vol_type
        else:
            return 'raw'

    def get_volume_path(self,volume):
        storages = self.get_storages()
        for storage in storages:
            stg = self.get_storage(storage)
            if stg.info()[0] != 0:
                stg.refresh(0)
                for img in stg.listVolumes():
                    if img == volume:
                        vol = stg.storageVollLookupByName(img)
                        return vol.path()

    def get_storage_by_vol_path(self,vol_path):
        vol = self.get_volume_by_path(vol_path)
        return vol.storagePoolLookupByVolume()

    def clone_from_template(self,clone,template,metadata=False):
        vol = self.get_volume_by_path(template)
        stg = vol.storagePoolLookupByVolume()
        storage_type = util.get_xml_path(stg.XMLDesc(0),"/pool/@type")
        format = util.get_xml_path(vol.XMLDesc(0),"/volume/target/format/@type")

        if storage_type == 'dir':
            clone += '.img'
        else:
            metadata = False
        xml = """
            <volume>
                <name>%s</name>
                <capacity>0</capacity>
                <allocation>0</allocation>
                <target>
                    <format type='%s' />
                </target>    
            </volume>
        """ % (clone,format)
        stg.createXMLFrom(xml,vol,metadata)
        clone_type = stg.storageVollLookupByName(clone)
        return clone_type.path()

    def _defineXML(self,xml):
        self.wvm.defineXML(xml)

    def delete_volume(self,path):
        vol = self.get_volume_by_path(path)
        vol.delete()

    def create_instance(self,name,memory,vcpu,host_model,uuid,images,cache_mode,networks,virtio,mac=None):
        #create vm function

        memory = int(memory) * 1024

        if self.get_kvm_supported():
            hypervisor_type = 'kvm'
        else:
            hypervisor_type = 'qemu'
        xml = """
                <domain type='%s'>
                    <name>%s</name>
                    <description>None</description>
                    <uuid>%s</uuid>
                    <memory unit='KiB'>%s</memory> 
                    <vcpu>%s</vcpu>
        """ % (hypervisor_type,name,uuid,memory,vcpu)

        if host_model:
            xml += """<cpu mode='host-model' />"""
        xml += """
                <os>
                    <type arch='%s'>%s</type>
                    <boot dev='hd' />
                    <boot dev='cdrom' />
                    <bootmenu enable='yes' />
                </os>
        """ % (self.get_host_arch(),self.get_os_type())

        xml += """
                <features>
                    <acpi/><apic><pae/>
                </features>
                <clock offset="utc" />
                <on_poweroff>destory</on_poweroff>
        """


