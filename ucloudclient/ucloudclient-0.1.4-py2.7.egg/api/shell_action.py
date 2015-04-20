import logging
import argparse

from ucloudclient.utils import api_utils
from ucloudclient.utils import shell_utils


logger = logging.getLogger(__name__)

'''
UHost
# CreateUHostInstance
# DescribeUHostInstance
# TerminateUHostInstance
# ResizeUHostInstance
# ReinstallUHostInstance
# StartUHostInstance
# StopUHostInstance
# RebootUHostInstance
# ResetUHostInstancePassword
# ModifyUHostInstanceName
ModifyUHostInstanceTag
ModifyUHostInstanceRemark
GetUHostInstancePrice
GetUHostInstanceVncInfo
DescribeImage
CreateCustomImage
TerminateCustomImage
AttachUDisk
DetachUDisk
CreateUHostInstanceSnapshot
DescribeUHostInstanceSnapshot
'''
def _key_value_pairing(text):
    try:
        (k, v) = text.split('=', 1)
        return (k, v)
    except ValueError:
        msg = "%r is not in the format of key=value" % text
        raise argparse.ArgumentTypeError(msg)


def _print_action_result(d):
    for i in d:
        if 'Id' in i:
            print('ID:%s\nOperated Sucessfully!!'%d[i])
    return 0


def _print_dict(d):
    '''
    print key value table
    '''
    shell_utils.print_dict(d)

def _print_origin_dict(d):
    shell_utils.print_original_dict(d)


def _print_host(d):
    # d={u'Remark': u'', u'Tag': u'Default', u'Name': u'yan-1',
    #     u'DiskSet': [{u'Type': u'Boot', u'Drive': u'/dev/sda',
    #     u'DiskId': u'ce3b1751-d837-4949-9c73-29368b7fe820',
    #     u'Size': 20}], u'IPSet': [{u'IP': u'10.11.1.126', u'Type': u'Private'},
    #     {u'IPId': u'eip-yci4qr', u'IP': u'107.150.97.103', u'Bandwidth': 2,
    #     u'Type': u'International'}], u'CPU': 1, u'State': u'Running',
    #     u'BasicImageId': u'uimage-nhwrqn', u'ImageId': u'ce3b1751-d837-4949-9c73-29368b7fe820',
    #     u'ExpireTime': 1429632272, u'UHostType': u'Normal', u'UHostId': u'uhost-4dmzop',
    #     u'NetworkState': u'Connected', u'ChargeType': u'Month', u'Memory': 2048,
    #     u'OsType': u'Linux', u'CreateTime': 1426953872, u'BasicImageName': u'Ubuntu 14.04 64\u4f4d'}
    # import pdb
    # pdb.set_trace()
    disk_set=d.pop('DiskSet')
    ip_set=d.pop('IPSet')
    if d.get('ExpireTime'):
        d['ExpireTime']= api_utils.get_formate_time(d['ExpireTime'])
    if d.get('CreateTime'):
        d['CreateTime']= api_utils.get_formate_time(d['CreateTime'])

    for i in range(len(disk_set)):
        disk=disk_set[i]
        exp_time=disk.get('ExpireTime')
        exp=''
        if exp_time:
            exp=" Exp:" + str(api_utils.get_formate_time(exp_time))
        disk_detail="%s %dGB Type:%s ID:%s %s"%(disk['Drive'],disk['Size'],disk['Type'],disk['DiskId'],exp)
        d['Disk_%d'%i]=disk_detail
    for j in range(len(ip_set)):
        ip=ip_set[j]
        bandwidth=''
        if ip.get('Bandwidth'):
            bandwidth=str(ip.get('Bandwidth',''))+"Mb/s"
        ip_id=''
        if ip.get('IPId'):
            ip_id="ID:"+str(ip.get('IPId'))
        ip_detail="%s %s %s %s"%(ip['Type'],bandwidth,ip['IP'],ip_id)
        d['IP_%d'%j]=ip_detail
    shell_utils.print_dict(d)


@shell_utils.arg(
    '--name',
    default=None,
    metavar='<name>',
    help=("Name of host."))
@shell_utils.arg(
    'imageid',
    metavar='<imageid>',
    help=("imageid of host."))
@shell_utils.arg(
    'loginmode',
    metavar='<loginmode>',
    help=("loginmode of host."))
@shell_utils.arg(
    '--loginmode',
    default=None,
    metavar='<loginmode>',
    help=("loginmode of host."))
@shell_utils.arg(
    '--password',
    default=None,
    metavar='<password>',
    help=("passwofd of host."))
@shell_utils.arg(
    '--keypair',
    default=None,
    metavar='<keypair>',
    help=("keypair of host."))
@shell_utils.arg(
    '--cpu',
    default=None,
    type=int,
    metavar='<cpu>',
    help=("cpu of host."))
@shell_utils.arg(
    '--memory',
    default=None,
    type=int,
    metavar='<memory>',
    help=("memory of host."))
@shell_utils.arg(
    '--diskspace',
    default=None,
    type=int,
    metavar='<diskspace>',
    help=("diskspace of host."))
@shell_utils.arg(
    '--networkid',
    default=None,
    metavar='<networkid>',
    help=("networkid of host."))
@shell_utils.arg(
    '--securitygroupid',
    default=None,
    metavar='<securitygroupid>',
    help=("securitygroupid of host."))
@shell_utils.arg(
    '--chargetype',
    default=None,
    metavar='<chargetype>',
    help=("chargetype of host."))
@shell_utils.arg(
    '--quantity',
    default=None,
    metavar='<quantity>',
    help=("quantity of host."))
def do_uhost_create(cs,args):
    '''
    boot a host
    '''
    result=cs.uhost.create(args.ucloud_region,args.imageid,args.loginmode)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
def do_uhost_show(cs,args):
    '''
    show detail of a host
    '''

    host=cs.uhost.get(args.ucloud_region,
                      [args.uhostid]).get('UHostSet')[0]
    _print_host(host)

@shell_utils.arg(
    '--offset',
    default=None,
    metavar='<offset>',
    help=("offset of return."))
@shell_utils.arg(
    '--limit',
    default=None,
    metavar='<limit>',
    help=("limit of return."))
def do_uhost_list(cs,args):
    '''
    list  uhosts
    '''

    uhosts = cs.uhost.get(args.ucloud_region,offset=args.offset,limit=args.limit).get('UHostSet')
    shell_utils.print_list(uhosts,['Name','UHostId','Tag','State',
                                   'BasicImageName'])


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
def do_uhost_start(cs,args):
    '''
    start a host
    '''
    
    result=cs.uhost.start(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
def do_uhost_stop(cs,args):
    '''
    stop a host
    '''
    
    result=cs.uhost.stop(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
def do_uhost_terminate(cs,args):
    '''
    terminate a host
    '''
    
    result=cs.uhost.terminate(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--cpu',
    default=None,
    type=int,
    metavar='<cpu>',
    help=("cpu of host."))
@shell_utils.arg(
    '--memory',
    default=None,
    type=int,
    metavar='<memory>',
    help=("memory of host."))
@shell_utils.arg(
    '--diskspace',
    default=None,
    type=int,
    metavar='<diskspace>',
    help=("diskspace of host."))
def do_uhost_resize(cs,args):
    '''
    resize a host
    '''
    
    result=cs.uhost.resize(args.ucloud_region,args.uhostid,args.cpu,
                           args.memory,args.diskspace)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--imageid',
    default=None,
    metavar='<imageid>',
    help=("imageid of host."))
@shell_utils.arg(
    '--password',
    default=None,
    metavar='<password>',
    help=("password of host."))
@shell_utils.arg(
    '--reservedisk',
    default=True,
    metavar='<reservedisk>',
    help=("reserve disk of not."))
def do_uhost_reinstall(cs,args):
    '''
    reinstall a host
    '''
    
    result=cs.uhost.reinstall(args.ucloud_region,args.uhostid,args.password,
                              args.imageid,args.reservedisk)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
@shell_utils.arg(
    'password',
    metavar='<password>',
    help=("password of host."))
def do_uhost_reset_password(cs,args):
    '''
    reset a host's password
    '''
    
    result=cs.uhost.reset_password(args.ucloud_region,args.uhostid,args.password)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
def do_uhost_reboot(cs,args):
    '''
    reboot a host
    '''
    
    result=cs.uhost.reboot(args.ucloud_region,args.uhostid)
    _print_action_result(result)

@shell_utils.arg(
    '--imagetype',
    default=None,
    metavar='<image type>',
    help=("imagetype."))
@shell_utils.arg(
    '--ostype',
    default=None,
    metavar='<os type>',
    help=("operating system type."))
@shell_utils.arg(
    '--imageid',
    default=None,
    metavar='<image id>',
    help=("imageid."))
@shell_utils.arg(
    '--offset',
    default=None,
    metavar='<offset>',
    help=("offset."))
@shell_utils.arg(
    '--limit',
    default=None,
    metavar='<limit>',
    help=("limit."))
def do_uhost_image_list(cs,args):
    '''
    list all images
    '''
    images=cs.uhost.get_image(args.ucloud_region,args.imagetype,args.ostype,
                              args.imageid,args.offset,
                              args.limit).get('ImageSet')
    shell_utils.print_list(images,['ImageId','ImageName','OsType'])



@shell_utils.arg(
    'imageid',
    default=None,
    metavar='<imageid>',
    help=(" image ."))
def do_uhost_image_show(cs,args):
    '''
    show image details
    '''
    images=cs.uhost.get_image(args.ucloud_region,image_id=args.imageid).get('ImageSet')[0]
    _print_dict(images)

@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
@shell_utils.arg(
    'name',
    metavar='<name>',
    help=("new name of host."))
def do_uhost_modify_name(cs,args):
    '''
    modify a host's name
    '''
    
    result=cs.uhost.modify_name(args.ucloud_region,args.uhostid,args.name)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhost id>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--tag',
    default=None,
    metavar='<tag>',
    help=("new tag of host."))
def do_uhost_modify_tag(cs,args):
    '''
    modify a host's tag
    '''
    
    result=cs.uhost.modify_name(args.ucloud_region,args.uhostid,args.tag)
    _print_action_result(result)



@shell_utils.arg(
    'imageid',
    metavar='<imageid>',
    help=("imageid of host."))
@shell_utils.arg(
    'cpu',
    type=int,
    metavar='<cpu>',
    help=("cpu of host."))
@shell_utils.arg(
    'memory',
    type=int,
    metavar='<memory>',
    help=("memory of host."))
@shell_utils.arg(
    'count',
    metavar='<count>',
    help=("count of host."))
@shell_utils.arg(
    '--chargetype',
    default=None,
    metavar='<chargetype>',
    help=("chargetype of host."))
@shell_utils.arg(
    '--diskspace',
    default=None,
    type=int,
    metavar='<diskspace>',
    help=("diskspace of host."))
def do_uhost_get_price(cs,args):
    '''
    get price of given type of host/s
    '''
    
    result=cs.uhost.get_price(args.ucloud_region,args.imageid,args.cpu,
                              args.memory,args.count,args.chargetype,
                              args.diskspace)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
def do_uhost_get_vnc(cs,args):
    '''
    get a host's vnc connection information
    '''
    
    result=cs.uhost.get_vnc(args.ucloud_region,args.uhostid)
    _print_dict(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--imagename',
    default=None,
    metavar='<imagename>',
    help=("imagename of new image."))
@shell_utils.arg(
    '--image_desc',
    default=None,
    metavar='<image_desc>',
    help=("image_desc of image."))
def do_uhost_create_image(cs,args):
    '''
    create an image from a given host
    '''
    
    result=cs.uhost.create_image(args.ucloud_region,args.uhostid,args.imageid,
                            args.image_desc)
    _print_action_result(result)


@shell_utils.arg(
    'imageid',
    metavar='<imageid>',
    help=("imageid of host."))
def do_uhost_delete_image(cs,args):
    '''
    delete an image by id
    '''
    
    result=cs.uhost.delete_image(args.ucloud_region,args.imageid)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
@shell_utils.arg(
    'udiskid',
    metavar='<udiskid>',
    help=("udiskid of host."))
def do_uhost_attach_disk(cs,args):
    '''
    attach a disk to a host
    '''
    
    result=cs.uhost.attach_disk(args.ucloud_region,args.uhostid,args.udiskid)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
@shell_utils.arg(
    'udiskid',
    metavar='<udiskid>',
    help=("udiskid of host."))
def do_uhost_detach_disk(cs,args):
    '''
    attach a disk to a host
    '''
    
    result=cs.uhost.detach_disk(args.ucloud_region,args.uhostid,args.udiskid)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
def do_uhost_create_snapshot(cs,args):
    '''
    create a snapshot from a host
    '''
    
    result=cs.uhost.create_snapshot(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    'uhostid',
    metavar='<uhost id>',
    help=("uhostid of host."))
def do_uhost_list_snapshot(cs,args):
    '''
    list snapshots of an instance
    '''
    
    result=cs.uhost.list_snapshot(args.ucloud_region,args.uhostid)
    _print_origin_dict(result)


@shell_utils.arg(
    'metric',
    metavar='<metrics>',
    help=("metrics name"))
@shell_utils.arg(
    'resourceid',
    metavar='<resourceid>',
    help=("resourceid of metric."))
@shell_utils.arg(
    'resource_type',
    metavar='<resource_type>',
    help=("uhosresource_typetid of metric."))
@shell_utils.arg(
    '--time_range',
    default=None,
    metavar='<time_range>',
    help=("time_range of metric."))
@shell_utils.arg(
    '--begin_time',
    default=None,
    metavar='<begin_time>',
    help=("begin_time of metric."))
@shell_utils.arg(
    '--end_time',
    default=None,
    metavar='<end_time>',
    help=("end_time of metric."))
def do_umon_metric_get(cs,args):
    '''
    get metic data
    '''
    result=cs.umon.metric_get(args.ucloud_region,args.metric,args.resourceid,
                              args.resource_type,args.time_range,
                              args.begin_time,args.end_time)
    _print_origin_dict(result)


@shell_utils.arg(
    'operator_name',
    metavar='<operator_name>',
    help=("operator name."))
@shell_utils.arg(
    'bandwidth',
    metavar='<bandwidth>',
    help=("bandwidth of elastic ip."))
@shell_utils.arg(
    '--charge_type',
    default=None,
    metavar='<charge_type>',
    help=("charge_type of elastic ip."))
@shell_utils.arg(
    '--quantity',
    default=None,
    metavar='<quantity>',
    help=("quantity of elastic ip."))
def do_unet_eip_create(cs,args):
    '''
    create an eip
    '''
    
    result=cs.unet.eip_create(args.ucloud_region,args.operator_name,
                              args.bandwidth,args.charge_type,args.quantity)
    _print_origin_dict(result)


@shell_utils.arg(
    '--offset',
    default=None,
    metavar='<offset>',
    help=("offset of return."))
@shell_utils.arg(
    '--limit',
    default=None,
    metavar='<limit>',
    help=("limit of return."))
def do_unet_eip_list(cs,args):
    '''
    list eip
    '''

    result=cs.unet.eip_get(args.ucloud_region,
                              args.offset,args.limit).get('EIPSet')
    for eip in result:
        ip=eip.get('EIPAddr')[0]
        eip.update(ip)
    shell_utils.print_list(result,['Name','EIPId','Bandwidth','IP','OperatorName'])


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("eip id"))
def do_unet_eip_show(cs,args):
    '''
    show eip details info
    '''

    result=cs.unet.eip_get(args.ucloud_region,args.id)
    _print_origin_dict(result)


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("eip id"))
@shell_utils.arg(
    '--name',
    default=None,
    metavar='<name>',
    help=("name of eip."))
@shell_utils.arg(
    '--tag',
    default=None,
    metavar='<tag>',
    help=("tag of eip."))
@shell_utils.arg(
    '--remark',
    default=None,
    metavar='<remark>',
    help=("remark of eip."))
def do_unet_eip_update(cs,args):
    '''
    update an eip
    '''
    result=cs.unet.eip_update(args.ucloud_region,args.id,
                              args.name,args.tag,args.remark)
    _print_action_result(result)


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("id of eip."))
def do_unet_eip_release(cs,args):
    '''
    release an eip
    '''
    
    result=cs.unet.eip_release(args.ucloud_region,args.id,)
    _print_action_result(result)


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("id of eip."))
@shell_utils.arg(
    'resource_type',
    metavar='<resource_type>',
    help=("resource_type."))
@shell_utils.arg(
    'reource_id',
    metavar='<reource_id>',
    help=("reource_id."))
def do_unet_eip_bind(cs,args):
    '''
    bind ip to given resource
    '''
    
    result=cs.unet.eip_bind(args.ucloud_region,args.id,
                              args.resource_type,args.reource_id)
    _print_action_result(result)


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("id of eip."))
@shell_utils.arg(
    'resource_type',
    metavar='<resource_type>',
    help=("resource_type."))
@shell_utils.arg(
    'reource_id',
    metavar='<reource_id>',
    help=("reource_id."))
def do_unet_eip_unbind(cs,args):
    '''
    unbind ip to given resource
    '''
    
    result=cs.unet.eip_unbind(args.ucloud_region,args.id,
                              args.resource_type,args.reource_id)
    _print_action_result(result)


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("id of eip."))
@shell_utils.arg(
    'bandwidth',
    metavar='<bandwidth>',
    help=("bandwidth of eip."))
def do_unet_eip_bandwidth_modify(cs,args):
    '''
    modify bandwidth of a given eip
    '''
    
    result=cs.unet.eip_bandwidth_modify(args.ucloud_region,args.id,
                              args.bandwidth)
    _print_action_result(result)


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("id of eip."))
@shell_utils.arg(
    'weight',
    metavar='<weight>',
    help=("weight of eip."))
def do_unet_eip_weight_modify(cs,args):
    '''
    modify weight of a given eip
    '''
    
    result=cs.unet.eip_weight_modify(args.ucloud_region,args.id,
                              args.weight)
    _print_action_result(result)


@shell_utils.arg(
    'operator_name',
    metavar='<operator_name>',
    help=("operator_name of eip."))
@shell_utils.arg(
    'bandwidth',
    metavar='<bandwidth>',
    help=("bandwidth of eip."))
@shell_utils.arg(
    '--charge_type',
    default=None,
    metavar='<charge_type>',
    help=("charge_type of eip."))
def do_unet_eip_price_get(cs,args):
    '''
    get eip price
    '''
    
    result=cs.unet.eip_price_get(args.ucloud_region,args.id,
                              args.weight)
    _print_origin_dict(result)


@shell_utils.arg(
    'count',
    metavar='<count>',
    help=("count of vip."))
def do_unet_vip_allocate(cs,args):
    '''
    allocate a vip
    '''
    
    result=cs.unet.vip_allocate(args.ucloud_region,args.count)
    _print_origin_dict(result)


def do_unet_vip_list(cs,args):
    '''
    list  vip
    '''
    vips=[]
    result=cs.unet.vip_get(args.ucloud_region).get('DataSet')
    for vip in result:
        vips.append({'virtual ip':vip})
    shell_utils.print_list(vips,['virtual ip'])


@shell_utils.arg(
    'vip_address',
    metavar='<vip>',
    help=("vip address."))
def do_unet_vip_release(cs,args):
    '''
    release a vip
    '''
    
    result=cs.unet.vip_release(args.ucloud_region,args.vip_address)
    _print_action_result(result)


@shell_utils.arg(
    '--resource_type',
    default=None,
    metavar='<resource_type>',
    help=("resource_type of security group."))
@shell_utils.arg(
    '--resource_id',
    default=None,
    metavar='<resource_id>',
    help=("resource_id of security group."))
def do_unet_sec_list(cs,args):
    '''
    get security group info.you can filte by reource id or resource type.
    '''
    
    result=cs.unet.sec_get(args.ucloud_region,args.resource_type,
                              args.resource_id).get('DataSet')
    shell_utils.print_list(result,['GroupName','GroupId','Type'])


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("id of security group."))
def do_unet_sec_show(cs,args):
    '''
    get security group details info.
    '''

    result=cs.unet.sec_get(args.ucloud_region,groupid=args.id).get('DataSet')
    _print_origin_dict(result)


@shell_utils.arg(
    'id',
    metavar='<sec_group_id>',
    help=("group_id of security group."))
def do_unet_sec_resource_get(cs,args):
    '''
    get resource attached to given security group
    '''
    
    result=cs.unet.sec_reource_get(args.ucloud_region,args.id).get('')
    _print_origin_dict(result)


@shell_utils.arg(
    'name',
    metavar='<name>',
    help=("name of security group."))
@shell_utils.arg(
    'desciption',
    default=None,
    metavar='<desciption>',
    help=("desciption of security group."))
@shell_utils.arg(
    'rule',
    nargs='+',
    metavar='<rule>',
    help=("rule of security group,structure of a rule:'Proto|Dst_port|Src_ip|"
          "Action|Priority' eg.UDP|53|0.0.0.0/0|ACCEPT|50T"))
def do_unet_sec_create(cs,args):
    '''
    create security group
    '''

    result=cs.unet.sec_creat(args.ucloud_region,args.name,args.rule,
                             args.desciption)
    _print_action_result(result)


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("id of security group."))
@shell_utils.arg(
    'rule',
    nargs='+',
    metavar='<rule>',
    help=("rule of security group,structure of a rule:'Proto|Dst_port|Src_ip|"
          "Action|Priority' eg.UDP|53|0.0.0.0/0|ACCEPT|50T"))
def do_unet_sec_update(cs,args):
    '''
    update security group
    '''

    result=cs.unet.sec_update(args.ucloud_region,args.id,args.rule)
    _print_action_result(result)


@shell_utils.arg(
    'id',
    metavar='<id>',
    help=("id of security group."))
@shell_utils.arg(
    'resource_type',
    metavar='<resource_type>',
    help=("resource_type of security group."))
@shell_utils.arg(
    'resource_id',
    metavar='<resource_id>',
    help=("resource_id"))
def do_unet_sec_grant(cs,args):
    '''
    grant given security group to specified resource
    '''
    
    result=cs.unet.sec_grant(args.ucloud_region,args.id,args.resource_type,
                             args.resource_id)
    _print_action_result(result)


@shell_utils.arg(
    'id',
    metavar='<sec_group_id>',
    help=("id of security group."))
def do_unet_sec_delete(cs,args):
    '''
    delete given security group
    '''
    
    result=cs.unet.sec_delete(args.ucloud_region,args.id)
    _print_action_result(result)
