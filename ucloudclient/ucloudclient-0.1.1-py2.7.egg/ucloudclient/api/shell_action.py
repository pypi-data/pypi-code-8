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
    return shell_utils.print_dict(d)

def _print_origin_dict(d):
    return shell_utils.print_original_dict(d)


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
    '--imageid',
    default=None,
    metavar='<imageid>',
    help=("imageid of host."))
@shell_utils.arg(
    '--loginmode',
    default=None,
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
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
def do_uhost_start(cs,args):
    '''
    start a host
    '''
    
    result=cs.uhost.start(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
def do_uhost_stop(cs,args):
    '''
    stop a host
    '''
    
    result=cs.uhost.stop(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
def do_uhost_terminate(cs,args):
    '''
    terminate a host
    '''
    
    result=cs.uhost.terminate(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
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
    '--uhostid',
    default=None,
    metavar='<uhostid>',
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
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--password',
    default=None,
    metavar='<password>',
    help=("password of host."))
def do_uhost_reset_password(cs,args):
    '''
    reset a host's password
    '''
    
    result=cs.uhost.reset_password(args.ucloud_region,args.uhostid,args.password)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
def do_uhost_reboot(cs,args):
    '''
    reboot a host
    '''
    
    result=cs.uhost.reboot(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
def do_uhost_show(cs,args):
    '''
    show detail of a host
    '''
    
    host=cs.uhost.get(args.ucloud_region,
                      [args.uhostid]).get('UHostSet')[0]
    _print_host(host)


def do_uhost_list(cs,args):
    '''
    list  uhosts
    '''
    
    uhosts = cs.uhost.get(args.ucloud_region).get('UHostSet')
    shell_utils.print_list(uhosts,['UHostId','Name','Tag','State',
                                   'BasicImageName'])


def do_uhost_image_list(cs,args):
    '''
    list all images
    '''
    images=cs.uhost.get_image(args.ucloud_region).get('ImageSet')
    shell_utils.print_list(images,['ImageId','ImageName','OsType'])


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--name',
    default=None,
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
    metavar='<uhostid>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--tag',
    default=None,
    metavar='<tag>',
    help=("new tag of host."))
def do_uhost_modify_name(cs,args):
    '''
    modify a host's tag
    '''
    
    result=cs.uhost.modify_name(args.ucloud_region,args.uhostid,args.tag)
    _print_action_result(result)



@shell_utils.arg(
    '--imageid',
    default=None,
    metavar='<imageid>',
    help=("imageid of host."))
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
    '--count',
    default=None,
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
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
def do_uhost_get_vnc(cs,args):
    '''
    get a host's vnc connection information
    '''
    
    result=cs.uhost.get_vnc(args.ucloud_region,args.uhostid)
    _print_dict(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--imageid',
    default=None,
    metavar='<imageid>',
    help=("imageid of host."))
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
    '--imageid',
    default=None,
    metavar='<imageid>',
    help=("imageid of host."))
def do_uhost_delete_image(cs,args):
    '''
    delete an image by id
    '''
    
    result=cs.uhost.delete_image(args.ucloud_region,args.imageid)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--udiskid',
    default=None,
    metavar='<udiskid>',
    help=("udiskid of host."))
def do_uhost_attach_disk(cs,args):
    '''
    attach a disk to a host
    '''
    
    result=cs.uhost.attach_disk(args.ucloud_region,args.uhostid,args.udiskid)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
@shell_utils.arg(
    '--udiskid',
    default=None,
    metavar='<udiskid>',
    help=("udiskid of host."))
def do_uhost_detach_disk(cs,args):
    '''
    attach a disk to a host
    '''
    
    result=cs.uhost.detach_disk(args.ucloud_region,args.uhostid,args.udiskid)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
def do_uhost_create_snapshot(cs,args):
    '''
    create a snapshot from a host
    '''
    
    result=cs.uhost.create_snapshot(args.ucloud_region,args.uhostid)
    _print_action_result(result)


@shell_utils.arg(
    '--uhostid',
    default=None,
    metavar='<uhostid>',
    help=("uhostid of host."))
def do_uhost_list_snapshot(cs,args):
    '''
    list snapshots of an instance
    '''
    
    result=cs.uhost.list_snapshot(args.ucloud_region,args.uhostid)
    _print_origin_dict(result)


@shell_utils.arg(
    '--metrics',
    default=None,
    metavar='<metrics>',
    help=("metrics name,if more than one metric,connect them with '&', eg.IORead&IOWrite..."))
@shell_utils.arg(
    '--resourceid',
    default=None,
    metavar='<resourceid>',
    help=("resourceid of metric."))
@shell_utils.arg(
    '--resource_type',
    default=None,
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
    
    metrics=None
    if args.metrics:
        metrics=args.metrics.split('&')
    result=cs.umon.metric_get(args.ucloud_region,metrics,args.resourceid,
                              args.resource_type,args.time_range,
                              args.begin_time,args.end_time)
    _print_origin_dict(result)


@shell_utils.arg(
    '--operator_name',
    default=None,
    metavar='<operator_name>',
    help=("operator name."))
@shell_utils.arg(
    '--bandwidth',
    default=None,
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
    '--id',
    default=None,
    metavar='<id>',
    help=("eip id, if more than one eip, connect them with '&', eg.ID-1&ID-2...."))
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
def do_unet_eip_get(cs,args):
    '''
    query eip in given id/s
    '''
    ids=None
    
    if args.id:
        ids=args.id.split('&')
    result=cs.unet.eip_get(args.ucloud_region,ids,
                              args.offset,args.limit)
    _print_origin_dict(result)


@shell_utils.arg(
    '--id',
    default=None,
    metavar='<id>',
    help=("eip id, if more than one eip, connect them with '&', eg.ID-1&ID-2...."))
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
    '--id',
    default=None,
    metavar='<id>',
    help=("id of eip."))
def do_unet_eip_release(cs,args):
    '''
    release an eip
    '''
    
    result=cs.unet.eip_release(args.ucloud_region,args.id,)
    _print_action_result(result)


@shell_utils.arg(
    '--id',
    default=None,
    metavar='<id>',
    help=("id of eip."))
@shell_utils.arg(
    '--resource_type',
    default=None,
    metavar='<resource_type>',
    help=("resource_type."))
@shell_utils.arg(
    '--reource_id',
    default=None,
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
    '--id',
    default=None,
    metavar='<id>',
    help=("id of eip."))
@shell_utils.arg(
    '--resource_type',
    default=None,
    metavar='<resource_type>',
    help=("resource_type."))
@shell_utils.arg(
    '--reource_id',
    default=None,
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
    '--id',
    default=None,
    metavar='<id>',
    help=("id of eip."))
@shell_utils.arg(
    '--bandwidth',
    default=None,
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
    '--id',
    default=None,
    metavar='<id>',
    help=("id of eip."))
@shell_utils.arg(
    '--weight',
    default=None,
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
    '--operator_name',
    default=None,
    metavar='<operator_name>',
    help=("operator_name of eip."))
@shell_utils.arg(
    '--bandwidth',
    default=None,
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
    '--count',
    default=None,
    metavar='<count>',
    help=("count of vip."))
def do_unet_vip_allocate(cs,args):
    '''
    allocate a vip
    '''
    
    result=cs.unet.vip_allocate(args.ucloud_region,args.count)
    _print_origin_dict(result)


def do_unet_vip_get(cs,args):
    '''
    list  vip
    '''
    
    result=cs.unet.vip_get(args.ucloud_region)
    _print_origin_dict(result)


@shell_utils.arg(
    '--vip_address',
    default=None,
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
@shell_utils.arg(
    '--group_id',
    default=None,
    metavar='<group_id>',
    help=("group_id of security group."))
def do_unet_sec_get(cs,args):
    '''
    get security group info
    '''
    
    result=cs.unet.sec_get(args.ucloud_region,args.resource_type,
                              args.resource_id,args.group_id)
    _print_origin_dict(result)


@shell_utils.arg(
    '--group_id',
    default=None,
    metavar='<group_id>',
    help=("group_id of security group."))
def do_unet_sec_reource_get(cs,args):
    '''
    get resource attached to given security group
    '''
    
    result=cs.unet.sec_reource_get(args.ucloud_region,args.group_id)
    _print_origin_dict(result)


@shell_utils.arg(
    '--name',
    default=None,
    metavar='<name>',
    help=("name of security group."))
@shell_utils.arg(
    '--desciption',
    default=None,
    metavar='<desciption>',
    help=("desciption of security group."))
@shell_utils.arg(
    '--rule',
    default=None,
    metavar='<rule>',
    help=("rule of security group,if more than one rule,connect them with '&',"
          "eg.UDP|53|0.0.0.0/0|ACCEPT|50&TCP|3306|0.0.0.0/0|DROP|50..."))
def do_unet_sec_creat(cs,args):
    '''
    create security group
    '''
    
    rules=None
    if args.rule:
        rules=args.rule.split('&')
    result=cs.unet.sec_creat(args.ucloud_region,args.name,rules,
                             args.desciption)
    _print_action_result(result)


@shell_utils.arg(
    '--id',
    default=None,
    metavar='<id>',
    help=("id of security group."))
@shell_utils.arg(
    '--rule',
    default=None,
    metavar='<rule>',
    help=("rule of security group,if more than one rule,connect them with '&',"
          "eg.UDP|53|0.0.0.0/0|ACCEPT|50&TCP|3306|0.0.0.0/0|DROP|50..."))
def do_unet_sec_update(cs,args):
    '''
    update security group
    '''
    
    rules=None
    if args.rule:
        rules=args.rule.split('&')
    result=cs.unet.sec_update(args.ucloud_region,args.id,rules)
    _print_action_result(result)


@shell_utils.arg(
    '--id',
    default=None,
    metavar='<id>',
    help=("id of security group."))
@shell_utils.arg(
    '--resource_type',
    default=None,
    metavar='<resource_type>',
    help=("resource_type of security group."))
@shell_utils.arg(
    '--resource_id',
    default=None,
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
    '--id',
    default=None,
    metavar='<id>',
    help=("id of security group."))
def do_unet_sec_delete(cs,args):
    '''
    delete given security group
    '''
    
    result=cs.unet.sec_delete(args.ucloud_region,args.id)
    _print_action_result(result)
