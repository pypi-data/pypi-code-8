#!/usr/bin/env python
#coding:utf-8
import sqlalchemy
import warnings
warnings.simplefilter('ignore', sqlalchemy.exc.SAWarning)
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy.orm import scoped_session, sessionmaker
from hashlib import md5
from toughradius.console.libs import utils
import functools

DeclarativeBase = declarative_base()


def get_metadata(db_engine):
    global DeclarativeBase
    metadata = DeclarativeBase.metadata
    metadata.bind = db_engine
    return metadata

class SlcNode(DeclarativeBase):
    """区域表"""
    __tablename__ = 'slc_node'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"区域编号")
    node_name = Column(u'node_name', Unicode(length=32), nullable=False,doc=u"区域名")
    node_desc = Column(u'node_desc', Unicode(length=64), nullable=False,doc=u"区域描述")

    #relation definitions

class SlcOperator(DeclarativeBase):
    """操作员表 操作员类型 0 系统管理员 1 普通操作员"""
    __tablename__ = 'slc_operator'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"操作员id")
    operator_type = Column('operator_type', INTEGER(), nullable=False,doc=u"操作员类型")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    operator_pass = Column(u'operator_pass', Unicode(length=128), nullable=False,doc=u"操作员密码")
    operator_status = Column(u'operator_status', INTEGER(), nullable=False,doc=u"操作员状态,0/1")
    operator_desc = Column(u'operator_desc', Unicode(255), nullable=False,doc=u"操作员描述")
    
class SlcOperatorNodes(DeclarativeBase):
    """操作员表关联区域"""
    __tablename__ = 'slc_operator_nodes'

    __table_args__ = {}

    #column definitions
    operator_name = Column(u'operator_name', Unicode(32),primary_key=True,nullable=False,doc=u"操作员名称")
    node_name = Column(u'node_name', Unicode(32), primary_key=True,nullable=False,doc=u"区域名称")

class SlcOperatorRule(DeclarativeBase):
    """操作员权限表"""
    __tablename__ = 'slc_operator_rule'

    __table_args__ = {}
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"权限id")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    rule_path = Column(u'rule_path', Unicode(128), nullable=False,doc=u"权限URL")
    rule_name = Column(u'rule_name', Unicode(128), nullable=False,doc=u"权限名称")
    rule_category = Column(u'rule_category', Unicode(128), nullable=False,doc=u"权限分类")


class SlcParam(DeclarativeBase):
    """系统参数表  <radiusd default table>"""
    __tablename__ = 'slc_param'

    __table_args__ = {}

    #column definitions
    param_name = Column(u'param_name', Unicode(length=64), primary_key=True, nullable=False,doc=u"参数名")
    param_value = Column(u'param_value', Unicode(length=255), nullable=False,doc=u"参数值")
    param_desc = Column(u'param_desc', Unicode(length=255),doc=u"参数描述")

    #relation definitions

class SlcRadBas(DeclarativeBase):
    """BAS设备表 <radiusd default table>"""
    __tablename__ = 'slc_rad_bas'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"设备id")
    vendor_id = Column(u'vendor_id', Unicode(length=32), nullable=False,doc=u"厂商标识")
    ip_addr = Column(u'ip_addr', Unicode(length=15), nullable=False,doc=u"IP地址")
    bas_name = Column(u'bas_name', Unicode(length=64), nullable=False,doc=u"bas名称")
    bas_secret = Column(u'bas_secret', Unicode(length=64), nullable=False,doc=u"共享密钥")
    coa_port = Column(u'coa_port', INTEGER(), nullable=False,doc=u"CoA端口")
    time_type = Column(u'time_type', SMALLINT(), nullable=False,doc=u"时区类型")

    #relation definitions



class SlcRadRoster(DeclarativeBase):
    """黑白名单 0 白名单 1 黑名单 <radiusd default table>"""
    __tablename__ = 'slc_rad_roster'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"黑白名单id")
    mac_addr = Column('mac_addr', Unicode(length=17), nullable=False,doc=u"mac地址")
    begin_time = Column('begin_time', Unicode(length=19), nullable=False,doc=u"生效开始时间")
    end_time = Column('end_time', Unicode(length=19), nullable=False,doc=u"生效结束时间")
    roster_type = Column('roster_type', SMALLINT(), nullable=False,doc=u"黑白名单类型")


class SlcMember(DeclarativeBase):
    """用户信息表"""
    __tablename__ = 'slc_member'

    __table_args__ = {}

    member_id = Column('member_id', INTEGER(),
        Sequence('member_id_seq', start=100001, increment=1),
        primary_key=True,nullable=False,doc=u"用户id")
    node_id = Column('node_id', INTEGER(), nullable=False,doc=u"区域id")
    member_name = Column('member_name', Unicode(length=64), nullable=False,doc=u"用户登录名")
    password = Column('password', Unicode(length=128), nullable=False,doc=u"用户登录密码")
    realname = Column('realname', Unicode(length=64), nullable=False,doc=u"")
    idcard = Column('idcard', Unicode(length=32),doc=u"用户证件号码")
    sex = Column('sex', SMALLINT(), nullable=True,doc=u"用户性别0/1")
    age = Column('age', INTEGER(), nullable=True,doc=u"用户年龄")
    email = Column('email', Unicode(length=255), nullable=True,doc=u"用户邮箱")
    email_active = Column('email_active', SMALLINT(), default=0,doc=u"用户邮箱激活状态")
    active_code =  Column('active_code', Unicode(length=32), nullable=False,doc=u"邮箱激活码")
    mobile = Column('mobile', Unicode(length=16), nullable=True,doc=u"用户手机")
    mobile_active = Column('mobile_active', SMALLINT(), default=0,doc=u"用户手机绑定状态")
    address = Column('address', Unicode(length=255), nullable=True,doc=u"用户地址")
    create_time = Column('create_time', Unicode(length=19), nullable=False,doc=u"创建时间")
    update_time = Column('update_time', Unicode(length=19), nullable=False,doc=u"更新时间")


class SlcMemberOrder(DeclarativeBase):
    """
    订购信息表(交易记录)
    pay_status交易支付状态：0-未支付，1-已支付，2-已取消
    """
    __tablename__ = 'slc_member_order'

    __table_args__ = {}

    order_id = Column('order_id', Unicode(length=32),primary_key=True,nullable=False,doc=u"订单id")
    member_id = Column('member_id', INTEGER(),nullable=False,doc=u"用户id")
    product_id = Column('product_id', INTEGER(),nullable=False,doc=u"资费id")
    account_number = Column('account_number', Unicode(length=32),nullable=False,doc=u"上网账号")
    order_fee = Column('order_fee', INTEGER(), nullable=False,doc=u"订单费用")
    actual_fee = Column('actual_fee', INTEGER(), nullable=False,doc=u"实缴费用")
    pay_status = Column('pay_status', INTEGER(), nullable=False,doc=u"支付状态")
    accept_id = Column('accept_id', INTEGER(),nullable=False,doc=u"受理id")
    order_source = Column('order_source', Unicode(length=64), nullable=False,doc=u"订单来源")
    order_desc = Column('order_desc', Unicode(length=255),doc=u"订单描述")
    create_time = Column('create_time', Unicode(length=19), nullable=False,doc=u"交易时间")


class SlcRechargerCard(DeclarativeBase):
    """
    充值卡表
    批次号：batch_no，以年月开始紧跟顺序号，如20150201
    卡类型 0 资费卡   1 余额卡
    状态 card_status 0 未激活 1 已激活 2 已使用 3 已回收
    """
    __tablename__ = 'slc_recharge_card'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"充值卡id")
    batch_no = Column('batch_no', INTEGER(), nullable=False,doc=u"批次号")
    card_number = Column('card_number', Unicode(length=16),nullable=False,unique=True,doc=u"充值卡号")
    card_passwd = Column('card_passwd', Unicode(length=128),nullable=False,doc=u"充值卡密码")
    card_type = Column('card_type', INTEGER(),nullable=False,doc=u"充值卡类型")
    card_status = Column('card_status', INTEGER(), nullable=False,doc=u"状态")
    product_id = Column('product_id', INTEGER(),nullable=True,doc=u"资费id")
    fee_value = Column('fee_value', INTEGER(), nullable=False,doc=u"充值卡面值-元")
    months = Column('months', INTEGER(),nullable=True,doc=u"授权月数")
    times = Column('times', INTEGER(),nullable=True,doc=u"授权时长(秒)")
    flows = Column('flows', INTEGER(),nullable=True,doc=u"授权流量(kb)")
    expire_date = Column('expire_date', Unicode(length=10), nullable=False,doc=u"过期时间- ####-##-##")
    create_time = Column('create_time', Unicode(length=19), nullable=False,doc=u"创建时间")

class SlcRechargeLog(DeclarativeBase):
    """
    充值记录
    """
    __tablename__ = 'slc_recharge_log'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"日志id")
    card_number = Column('card_number', Unicode(length=16),nullable=False,doc=u"充值卡号")
    member_id = Column('member_id', INTEGER(),nullable=False,doc=u"用户id")
    account_number = Column('account_number', Unicode(length=32),nullable=False,doc=u"上网账号")
    recharge_status = Column('recharge_status', INTEGER(), nullable=False,doc=u"充值结果")
    recharge_time = Column('recharge_time', Unicode(length=19), nullable=False,doc=u"充值时间")


class SlcRadAccount(DeclarativeBase):
    """
    上网账号表，每个会员可以同时拥有多个上网账号
    account_number 为每个套餐对应的上网账号，每个上网账号全局唯一
    用户状态 0:"预定",1:"正常", 2:"停机" , 3:"销户", 4:"到期"
    <radiusd default table>
    """

    __tablename__ = 'slc_rad_account'

    __table_args__ = {}

    account_number = Column('account_number', Unicode(length=32),primary_key=True,nullable=False,doc=u"上网账号")
    member_id = Column('member_id', INTEGER(),nullable=False,doc=u"用户id")
    product_id = Column('product_id', INTEGER(),nullable=False,doc=u"资费id")
    group_id = Column('group_id', INTEGER(),doc=u"用户组id")
    password = Column('password', Unicode(length=128), nullable=False,doc=u"上网密码")
    status = Column('status', INTEGER(), nullable=False,doc=u"用户状态")
    install_address = Column('install_address', Unicode(length=128), nullable=False,doc=u"装机地址")
    balance = Column('balance', INTEGER(), nullable=False,doc=u"用户余额-分")
    time_length = Column('time_length', INTEGER(), nullable=False,default=0,doc=u"用户时长-秒")
    flow_length = Column('flow_length', INTEGER(), nullable=False,default=0,doc=u"用户流量-kb")
    expire_date = Column('expire_date', Unicode(length=10), nullable=False,doc=u"过期时间- ####-##-##")
    user_concur_number = Column('user_concur_number', INTEGER(), nullable=False,doc=u"用户并发数")
    bind_mac = Column('bind_mac', SMALLINT(), nullable=False,doc=u"是否绑定mac")
    bind_vlan = Column('bind_vlan', SMALLINT(), nullable=False,doc=u"是否绑定vlan")
    mac_addr = Column('mac_addr', Unicode(length=17),doc=u"mac地址")
    vlan_id = Column('vlan_id', INTEGER(),doc=u"内层vlan")
    vlan_id2 = Column('vlan_id2', INTEGER(),doc=u"外层vlan")
    ip_address = Column('ip_address', Unicode(length=15),doc=u"静态IP地址")
    last_pause = Column('last_pause', Unicode(length=19),doc=u"最后停机时间")
    create_time = Column('create_time', Unicode(length=19), nullable=False,doc=u"创建时间")
    update_time = Column('update_time', Unicode(length=19), nullable=False,doc=u"更新时间")

class SlcRadAccountAttr(DeclarativeBase):
    """上网账号扩展策略属性表"""
    __tablename__ = 'slc_rad_account_attr'
    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"属性id")
    account_number = Column('account_number', Unicode(length=32),nullable=False,doc=u"上网账号")
    attr_name = Column(u'attr_name', Unicode(length=255), nullable=False,doc=u"属性名")
    attr_value = Column(u'attr_value', Unicode(length=255), nullable=False,doc=u"属性值")
    attr_desc = Column(u'attr_desc', Unicode(length=255),doc=u"属性描述")

class SlcRadProduct(DeclarativeBase):
    '''
    资费信息表 <radiusd default table>
    资费类型 product_policy 0 预付费包月 1 预付费时长 2 买断包月 3 买断时长 4 预付费流量 5 买断流量
    销售状态 product_status 0 正常 1 停用 资费停用后不允许再订购
    '''
    __tablename__ = 'slc_rad_product'

    __table_args__ = {}

    id = Column('id', INTEGER(),primary_key=True,autoincrement=1,nullable=False,doc=u"资费id")
    product_name = Column('product_name', Unicode(length=64), nullable=False,doc=u"资费名称")
    product_policy = Column('product_policy', INTEGER(), nullable=False,doc=u"资费策略")
    product_status = Column('product_status', SMALLINT(), nullable=False,doc=u"资费状态")
    bind_mac = Column('bind_mac', SMALLINT(), nullable=False,doc=u"是否绑定mac")
    bind_vlan = Column('bind_vlan', SMALLINT(), nullable=False,doc=u"是否绑定vlan")
    concur_number = Column('concur_number', INTEGER(), nullable=False,doc=u"并发数")
    fee_period = Column('fee_period', Unicode(length=11),doc=u"开放认证时段")
    fee_months = Column('fee_months', INTEGER(),doc=u"买断授权月数")
    fee_times = Column('fee_times', INTEGER(),doc=u"买断时长(秒)")
    fee_flows = Column('fee_flows', INTEGER(),doc=u"买断流量(kb)")
    fee_price = Column('fee_price', INTEGER(),nullable=False,doc=u"资费价格")
    input_max_limit = Column('input_max_limit', INTEGER(), nullable=False,doc=u"上行速率")
    output_max_limit = Column('output_max_limit', INTEGER(), nullable=False,doc=u"下行速率")
    create_time = Column('create_time', Unicode(length=19), nullable=False,doc=u"创建时间")
    update_time = Column('update_time', Unicode(length=19), nullable=False,doc=u"更新时间")

class SlcRadProductAttr(DeclarativeBase):
    '''资费扩展属性表 <radiusd default table>'''
    __tablename__ = 'slc_rad_product_attr'

    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"属性id")
    product_id = Column('product_id', INTEGER(),nullable=False,doc=u"资费id")
    attr_name = Column(u'attr_name', Unicode(length=255), nullable=False,doc=u"属性名")
    attr_value = Column(u'attr_value', Unicode(length=255), nullable=False,doc=u"属性值")
    attr_desc = Column(u'attr_desc', Unicode(length=255),doc=u"属性描述")

class SlcRadBilling(DeclarativeBase):
    """计费信息表 is_deduct 0 未扣费 1 已扣费 <radiusd default table>"""
    __tablename__ = 'slc_rad_billing'

    __table_args__ = { }

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"计费id")
    account_number = Column(u'account_number', Unicode(length=253), nullable=False,doc=u"上网账号")
    nas_addr = Column(u'nas_addr', Unicode(length=15), nullable=False,doc=u"bas地址")
    acct_session_id = Column(u'acct_session_id', Unicode(length=253), nullable=False,doc=u"会话id")
    acct_start_time = Column(u'acct_start_time', Unicode(length=19), nullable=False,doc=u"计费开始时间")
    acct_session_time = Column(u'acct_session_time', INTEGER(), nullable=False,doc=u"会话时长")
    input_total = Column(u'input_total', INTEGER(),doc=u"会话的上行流量（kb）")
    output_total = Column(u'output_total', INTEGER(),doc=u"会话的下行流量（kb）")
    acct_times = Column(u'acct_times', INTEGER(), nullable=False,doc=u"扣费时长(秒)")
    acct_flows = Column(u'acct_flows', INTEGER(), nullable=False,doc=u"扣费流量(kb)")
    acct_fee = Column(u'acct_fee', INTEGER(), nullable=False,doc=u"应扣费用")
    actual_fee = Column('actual_fee', INTEGER(), nullable=False,doc=u"实扣费用")
    balance = Column('balance', INTEGER(), nullable=False,doc=u"当前余额")
    time_length = Column('time_length', INTEGER(), nullable=False,default=0,doc=u"当前用户时长-秒")
    flow_length = Column('flow_length', INTEGER(), nullable=False,default=0,doc=u"当前用户流量-kb")
    is_deduct = Column(u'is_deduct', INTEGER(), nullable=False,doc=u"是否扣费")
    create_time = Column('create_time', Unicode(length=19), nullable=False,doc=u"计费时间")


class SlcRadTicket(DeclarativeBase):
    """上网日志表 <radiusd default table>"""
    __tablename__ = 'slc_rad_ticket'

    __table_args__ = { }

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"日志id")
    account_number = Column(u'account_number', Unicode(length=253), nullable=False,doc=u"上网账号")
    acct_input_gigawords = Column(u'acct_input_gigawords', INTEGER(),doc=u"会话的上行的字（4字节）的吉倍数")
    acct_output_gigawords = Column(u'acct_output_gigawords', INTEGER(),doc=u"会话的下行的字（4字节）的吉倍数")
    acct_input_octets = Column(u'acct_input_octets', INTEGER(),doc=u"会话的上行流量（字节数）")
    acct_output_octets = Column(u'acct_output_octets', INTEGER(),doc=u"会话的下行流量（字节数）")
    acct_input_packets = Column(u'acct_input_packets', INTEGER(),doc=u"会话的上行包数量")
    acct_output_packets = Column(u'acct_output_packets', INTEGER(),doc=u"会话的下行包数量")
    acct_session_id = Column(u'acct_session_id', Unicode(length=253), nullable=False,doc=u"会话id")
    acct_session_time = Column(u'acct_session_time', INTEGER(), nullable=False,doc=u"会话时长")
    acct_start_time = Column(u'acct_start_time', Unicode(length=19), nullable=False,doc=u"会话开始时间")
    acct_stop_time = Column(u'acct_stop_time', Unicode(length=19), nullable=False,doc=u"会话结束时间")
    acct_terminate_cause = Column(u'acct_terminate_cause',INTEGER(),doc=u"会话中止原因")
    mac_addr = Column(u'mac_addr', Unicode(length=128),doc=u"mac地址")
    calling_station_id =  Column(u'calling_station_id', Unicode(length=128),doc=u"用户接入物理信息")
    framed_netmask = Column(u'frame_id_netmask', Unicode(length=15),doc=u"地址掩码")
    framed_ipaddr = Column(u'framed_ipaddr', Unicode(length=15),doc=u"IP地址")
    nas_class = Column(u'nas_class', Unicode(length=253),doc=u"bas class")
    nas_addr = Column(u'nas_addr', Unicode(length=15), nullable=False,doc=u"bas地址")
    nas_port = Column(u'nas_port', Unicode(length=32),doc=u"接入端口")
    nas_port_id = Column(u'nas_port_id', Unicode(length=255),doc=u"接入端口物理信息")
    nas_port_type = Column(u'nas_port_type', INTEGER(),doc=u"接入端口类型")
    service_type = Column(u'service_type', INTEGER(),doc=u"接入服务类型")
    session_timeout = Column(u'session_timeout', INTEGER(),doc=u"会话超时时间")
    start_source = Column(u'start_source', INTEGER(), nullable=False,doc=u"会话开始来源")
    stop_source = Column(u'stop_source', INTEGER(), nullable=False,doc=u"会话中止来源")

    #relation definitions

class SlcRadOnline(DeclarativeBase):
    """用户在线信息表 <radiusd default table>"""
    __tablename__ = 'slc_rad_online'

    __table_args__ = {
        'mysql_engine' : 'MEMORY'
    }

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"在线id")
    account_number = Column(u'account_number', Unicode(length=32), nullable=False,doc=u"上网账号")
    nas_addr = Column(u'nas_addr', Unicode(length=32), nullable=False,doc=u"bas地址")
    acct_session_id = Column(u'acct_session_id', Unicode(length=64), nullable=False,doc=u"会话id")
    acct_start_time = Column(u'acct_start_time', Unicode(length=19), nullable=False,doc=u"会话开始时间")
    framed_ipaddr = Column(u'framed_ipaddr', Unicode(length=32), nullable=False,doc=u"IP地址")
    mac_addr = Column(u'mac_addr', Unicode(length=32), nullable=False,doc=u"mac地址")
    nas_port_id = Column(u'nas_port_id', Unicode(length=255), nullable=False,doc=u"接入端口物理信息")
    billing_times = Column(u'billing_times', INTEGER(), nullable=False,doc=u"已记账时间")
    input_total = Column(u'input_total', INTEGER(),doc=u"上行流量（kb）")
    output_total = Column(u'output_total', INTEGER(),doc=u"下行流量（kb）")
    start_source = Column(u'start_source', SMALLINT(), nullable=False,doc=u"记账开始来源")

class SlcRadOnlineStat(DeclarativeBase):
    """用户在线统计表 """
    __tablename__ = 'slc_rad_online_stat'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"id")
    node_id = Column('node_id', INTEGER(),nullable=False,doc=u"区域id")
    stat_time = Column(u'stat_time', INTEGER(),  nullable=False,doc=u"统计时间")
    total = Column(u'total', INTEGER(),doc=u"在线数")

    #relation definitions

class SlcRadFlowStat(DeclarativeBase):
    """用户在线统计表 """
    __tablename__ = 'slc_rad_flow_stat'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"id")
    node_id = Column('node_id', INTEGER(),nullable=False,doc=u"区域id")
    stat_time = Column(u'stat_time', INTEGER(),  nullable=False,doc=u"统计时间")
    input_total = Column(u'input_total', INTEGER(),doc=u"上行流量（kb）")
    output_total = Column(u'output_total', INTEGER(),doc=u"下行流量（kb）")

    #relation definitions

class SlcRadAcceptLog(DeclarativeBase):
    '''
    业务受理日志表
    open:开户 pause:停机 resume:复机 cancel:销户 next:续费 charge:充值
    '''
    __tablename__ = 'slc_rad_accept_log'
    __table_args__ = {}

    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"日志id")
    accept_type = Column(u'accept_type', Unicode(length=16), nullable=False,doc=u"受理类型")
    accept_desc = Column(u'accept_desc', Unicode(length=512),doc=u"受理描述")
    account_number = Column(u'account_number', Unicode(length=32), nullable=False,doc=u"上网账号")
    operator_name = Column(u'operator_name', Unicode(32),doc=u"操作员名")
    accept_source = Column(u'accept_source', Unicode(length=128),doc=u"受理渠道来源")
    accept_time = Column(u'accept_time', Unicode(length=19), nullable=False,doc=u"受理时间")

class SlcRadOperateLog(DeclarativeBase):
    """操作日志表"""
    __tablename__ = 'slc_rad_operate_log'

    __table_args__ = {}

    #column definitions
    id = Column(u'id', INTEGER(), primary_key=True, nullable=False,doc=u"日志id")
    operator_name = Column(u'operator_name', Unicode(32), nullable=False,doc=u"操作员名称")
    operate_ip = Column(u'operate_ip', Unicode(length=128),doc=u"操作员ip")
    operate_time = Column(u'operate_time', Unicode(length=19), nullable=False,doc=u"操作时间")
    operate_desc = Column(u'operate_desc', Unicode(length=1024),doc=u"操作描述")

def init_db(db):
    node = SlcNode()
    node.id = 1
    node.node_name = 'default'
    node.node_desc = u'测试区域'
    db.add(node)

    params = [
        ('system_name',u'管理系统名称',u'ToughRADIUS管理控制台'),
        ('customer_system_name',u'自助服务系统名称',u'ToughRADIUS自助服务中心'),
        ('customer_system_url',u"自助服务系统地址",u"http://forum.toughradius.net"),
        ('customer_must_active',u"激活邮箱才能自助开户充值(0:否|1:是)",u"0"),
        ('radiusd_address',u'Radius服务IP地址',u'127.0.0.1'),
        ('radiusd_admin_port',u'Radius服务管理端口',u'1815'),
        ('is_debug',u'DEBUG模式',u'0'),
        ('weixin_qrcode',u'微信公众号二维码图片(宽度230px)',u'http://img.toughradius.net/toughforum/jamiesun/1421820686.jpg!230'),
        ('service_phone',u'客户服务电话',u'000000'),
        ('service_qq',u'客户服务QQ号码',u'000000'),
        ('rcard_order_url',u'充值卡订购网站地址',u'http://www.tmall.com'),
        ('portal_secret',u'portal登陆密钥', u'abcdefg123456'),
        ('expire_notify_days','到期提醒提前天数',u'7'),
        ('expire_notify_tpl','到期提醒邮件模板',u'账号到期通知\n尊敬的会员您好:\n您的账号#account#即将在#expire#到期，请及时续费！'),
        ('expire_notify_url',u'到期通知url',u'http://your_notify_url?account={account}&expire={expire}&email={email}&mobile={mobile}'),
        ('expire_addrpool',u'到期提醒下发地址池',u'expire'),
        ('expire_session_timeout',u'到期用户下发最大会话时长(秒)',u'120'),
        ('smtp_server',u'SMTP服务器地址',u'smtp.mailgun.org'),
        ('smtp_user',u'SMTP用户名',u'service@toughradius.org'),
        ('smtp_pwd',u'SMTP密码',u'service2015'),
        ('smtp_sender',u'SMTP发送人名称',u'运营中心'),
        ('acct_interim_intelval',u'Radius记账间隔(秒)',u'120'),
        ('max_session_timeout',u'Radius最大会话时长(秒)',u'86400'),
        ('reject_delay',u'拒绝延迟时间(秒)(0-9)','0')
    ]

    for p in params:
        param = SlcParam()
        param.param_name = p[0]
        param.param_desc = p[1]
        param.param_value = p[2]
        db.add(param)

    opr = SlcOperator()
    opr.id = 1
    opr.operator_name = u'admin'
    opr.operator_type = 0
    opr.operator_pass = md5('root').hexdigest()
    opr.operator_desc = 'admin'
    opr.operator_status = 0
    db.add(opr)

    db.commit()
    db.close()

def update(db_engine):
    print 'starting update database...'
    metadata = get_metadata(db_engine)
    metadata.drop_all(db_engine)
    metadata.create_all(db_engine)
    print 'update database done'
    db = scoped_session(sessionmaker(bind=db_engine, autocommit=False, autoflush=True))()
    init_db(db)

if __name__ == '__main__':
    update()
