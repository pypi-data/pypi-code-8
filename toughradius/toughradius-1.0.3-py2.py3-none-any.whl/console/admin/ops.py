#!/usr/bin/env python
#coding:utf-8

from bottle import Bottle
from bottle import request
from bottle import response
from bottle import redirect
from bottle import static_file
from bottle import mako_template as render
from tablib import Dataset
from toughradius.console.websock import websock
from toughradius.console import models
from toughradius.console.libs import utils
from toughradius.console.base import *
from toughradius.console.admin import forms
import bottle
import datetime
from sqlalchemy import func

__prefix__ = "/ops"

app = Bottle()
app.config['__prefix__'] = __prefix__
render = functools.partial(Render.render_app,app)

###############################################################################
# user manage        
###############################################################################
                   
@app.route('/user',apply=auth_opr,method=['GET','POST'])
def user_query(db):   
    node_id = request.params.get('node_id')
    product_id = request.params.get('product_id')
    user_name = request.params.get('user_name')
    status = request.params.get('status')
    opr_nodes = get_opr_nodes(db)
    _query = db.query(
            models.SlcRadAccount,
            models.SlcMember.realname,
            models.SlcRadProduct.product_name
        ).filter(
            models.SlcRadProduct.id == models.SlcRadAccount.product_id,
            models.SlcMember.member_id == models.SlcRadAccount.member_id
        )
    if node_id:
        _query = _query.filter(models.SlcMember.node_id == node_id)
    else:
        _query = _query.filter(models.SlcMember.node_id.in_([i.id for i in opr_nodes]))
    if product_id:
        _query = _query.filter(models.SlcRadAccount.product_id==product_id)
    if user_name:
        _query = _query.filter(models.SlcRadAccount.account_number.like('%'+user_name+'%'))
    if status:
        _query = _query.filter(models.SlcRadAccount.status == status)

    if request.path == '/user':
        return render("ops_user_list", page_data = get_page_data(_query),
                       node_list=opr_nodes, 
                       product_list=db.query(models.SlcRadProduct),**request.params)
                       
permit.add_route("%s/user"%__prefix__,u"用户账号查询",u"运维管理",is_menu=True,order=0)

@app.get('/user/trace',apply=auth_opr)
def user_trace(db):   
    return render("ops_user_trace", bas_list=db.query(models.SlcRadBas))

permit.add_route("%s/user/trace"%__prefix__,u"用户消息跟踪",u"运维管理",is_menu=True,order=1)
                   
@app.get('/user/detail',apply=auth_opr)
def user_detail(db):   
    account_number = request.params.get('account_number')  
    user  = db.query(
        models.SlcMember.realname,
        models.SlcRadAccount.member_id,
        models.SlcRadAccount.account_number,
        models.SlcRadAccount.expire_date,
        models.SlcRadAccount.balance,
        models.SlcRadAccount.time_length,
        models.SlcRadAccount.flow_length,
        models.SlcRadAccount.user_concur_number,
        models.SlcRadAccount.status,
        models.SlcRadAccount.mac_addr,
        models.SlcRadAccount.vlan_id,
        models.SlcRadAccount.vlan_id2,
        models.SlcRadAccount.ip_address,
        models.SlcRadAccount.bind_mac,
        models.SlcRadAccount.bind_vlan,
        models.SlcRadAccount.ip_address,
        models.SlcRadAccount.install_address,
        models.SlcRadAccount.create_time,
        models.SlcRadProduct.product_name
    ).filter(
            models.SlcRadProduct.id == models.SlcRadAccount.product_id,
            models.SlcMember.member_id == models.SlcRadAccount.member_id,
            models.SlcRadAccount.account_number == account_number
    ).first()
    if not user:
        return render("error",msg=u"用户不存在")
    user_attrs = db.query(models.SlcRadAccountAttr).filter_by(account_number=account_number)
    return render("ops_user_detail",user=user,user_attrs=user_attrs)
    
permit.add_route("%s/user/detail"%__prefix__,u"账号详情",u"运维管理",order=1.01)

@app.post('/user/release',apply=auth_opr)
def user_release(db):   
    account_number = request.params.get('account_number')  
    user = db.query(models.SlcRadAccount).filter_by(account_number=account_number).first()
    user.mac_addr = ''
    user.vlan_id = 0
    user.vlan_id2 = 0

    ops_log = models.SlcRadOperateLog()
    ops_log.operator_name = get_cookie("username")
    ops_log.operate_ip = get_cookie("login_ip")
    ops_log.operate_time = utils.get_currtime()
    ops_log.operate_desc = u'释放用户账号（%s）绑定信息'%(account_number,)
    db.add(ops_log)

    db.commit()
    websock.update_cache("account",account_number=account_number)
    return dict(code=0,msg=u"解绑成功")
    
permit.add_route("%s/user/release"%__prefix__,u"用户释放绑定",u"运维管理",order=1.02)    

###############################################################################
# online manage      
###############################################################################
    
@app.route('/online',apply=auth_opr,method=['GET','POST'])
def online_query(db): 
    node_id = request.params.get('node_id')
    account_number = request.params.get('account_number')  
    framed_ipaddr = request.params.get('framed_ipaddr')  
    mac_addr = request.params.get('mac_addr')  
    nas_addr = request.params.get('nas_addr')  
    opr_nodes = get_opr_nodes(db)
    _query = db.query(
        models.SlcRadOnline.id,
        models.SlcRadOnline.account_number,
        models.SlcRadOnline.nas_addr,
        models.SlcRadOnline.acct_session_id,
        models.SlcRadOnline.acct_start_time,
        models.SlcRadOnline.framed_ipaddr,
        models.SlcRadOnline.mac_addr,
        models.SlcRadOnline.nas_port_id,
        models.SlcRadOnline.start_source,
        models.SlcRadOnline.billing_times,
        models.SlcRadOnline.input_total,
        models.SlcRadOnline.output_total,
        models.SlcMember.node_id,
        models.SlcMember.realname
    ).filter(
            models.SlcRadOnline.account_number == models.SlcRadAccount.account_number,
            models.SlcMember.member_id == models.SlcRadAccount.member_id
    )
    if node_id:
        _query = _query.filter(models.SlcMember.node_id == node_id)
    else:
        _query = _query.filter(models.SlcMember.node_id.in_([i.id for i in opr_nodes]))
            
    if account_number:
        _query = _query.filter(models.SlcRadOnline.account_number.like('%'+account_number+'%'))
    if framed_ipaddr:
        _query = _query.filter(models.SlcRadOnline.framed_ipaddr == framed_ipaddr)
    if mac_addr:
        _query = _query.filter(models.SlcRadOnline.mac_addr == mac_addr)
    if nas_addr:
        _query = _query.filter(models.SlcRadOnline.nas_addr == nas_addr)

    _query = _query.order_by(models.SlcRadOnline.acct_start_time.desc())
    return render("ops_online_list", page_data = get_page_data(_query),
                   node_list=opr_nodes, 
                   bas_list=db.query(models.SlcRadBas),**request.params)

permit.add_route("%s/online"%__prefix__,u"在线用户查询",u"运维管理",is_menu=True,order=2)

###############################################################################
# ticket manage        
###############################################################################

@app.route('/ticket',apply=auth_opr,method=['GET','POST'])
def ticket_query(db): 
    node_id = request.params.get('node_id')
    account_number = request.params.get('account_number')  
    framed_ipaddr = request.params.get('framed_ipaddr')  
    mac_addr = request.params.get('mac_addr')  
    query_begin_time = request.params.get('query_begin_time')  
    query_end_time = request.params.get('query_end_time')  
    opr_nodes = get_opr_nodes(db)
    _query = db.query(
        models.SlcRadTicket.id,
        models.SlcRadTicket.account_number,
        models.SlcRadTicket.nas_addr,
        models.SlcRadTicket.acct_session_id,
        models.SlcRadTicket.acct_start_time,
        models.SlcRadTicket.acct_stop_time,
        models.SlcRadTicket.acct_input_octets,
        models.SlcRadTicket.acct_output_octets,
        models.SlcRadTicket.acct_input_gigawords,
        models.SlcRadTicket.acct_output_gigawords,
        models.SlcRadTicket.framed_ipaddr,
        models.SlcRadTicket.mac_addr,
        models.SlcRadTicket.nas_port_id,
        models.SlcMember.node_id,
        models.SlcMember.realname
    ).filter(
            models.SlcRadTicket.account_number == models.SlcRadAccount.account_number,
            models.SlcMember.member_id == models.SlcRadAccount.member_id
    )
    if node_id:
        _query = _query.filter(models.SlcMember.node_id == node_id)
    else:
        _query = _query.filter(models.SlcMember.node_id.in_([i.id for i in opr_nodes]))
    if account_number:
        _query = _query.filter(models.SlcRadTicket.account_number.like('%'+account_number+'%'))
    if framed_ipaddr:
        _query = _query.filter(models.SlcRadTicket.framed_ipaddr == framed_ipaddr)
    if mac_addr:
        _query = _query.filter(models.SlcRadTicket.mac_addr == mac_addr)
    if query_begin_time:
        _query = _query.filter(models.SlcRadTicket.acct_start_time >= query_begin_time)
    if query_end_time:
        _query = _query.filter(models.SlcRadTicket.acct_stop_time <= query_end_time)

    _query = _query.order_by(models.SlcRadTicket.acct_start_time.desc())
    return render("ops_ticket_list", page_data = get_page_data(_query),
               node_list=opr_nodes,**request.params)

permit.add_route("%s/ticket"%__prefix__,u"上网日志查询",u"运维管理",is_menu=True,order=3)

###############################################################################
# ops log manage        
###############################################################################

@app.route('/opslog',apply=auth_opr,method=['GET','POST'])
def opslog_query(db): 
    operator_name = request.params.get('operator_name')
    query_begin_time = request.params.get('query_begin_time')  
    query_end_time = request.params.get('query_end_time')  
    keyword = request.params.get('keyword')
    opr_nodes = get_opr_nodes(db)
    _query = db.query(models.SlcRadOperateLog).filter(
        models.SlcRadOperateLog.operator_name == models.SlcOperator.operator_name,
    ) 
    if operator_name:
        _query = _query.filter(models.SlcRadOperateLog.operator_name == operator_name)
    if keyword:
        _query = _query.filter(models.SlcRadOperateLog.operate_desc.like("%"+keyword+"%"))        
    if query_begin_time:
        _query = _query.filter(models.SlcRadOperateLog.operate_time >= query_begin_time+' 00:00:00')
    if query_end_time:
        _query = _query.filter(models.SlcRadOperateLog.operate_time <= query_end_time+' 23:59:59')
    _query = _query.order_by(models.SlcRadOperateLog.operate_time.desc())
    return render("ops_log_list", 
        node_list=opr_nodes,
        page_data = get_page_data(_query),**request.params)


permit.add_route("%s/opslog"%__prefix__,u"操作日志查询",u"运维管理",is_menu=True,order=4)

###############################################################################
# ops log manage        
###############################################################################

def default_start_end():
    day_code = datetime.datetime.now().strftime("%Y-%m-%d")
    begin = datetime.datetime.strptime("%s 00:00:00"%day_code,"%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime("%s 23:59:59"%day_code,"%Y-%m-%d %H:%M:%S")
    return time.mktime(begin.timetuple()),time.mktime(end.timetuple())

@app.get('/online/stat',apply=auth_opr)
def online_stat_query(db): 
    return render(
        "ops_online_stat",
        node_list=get_opr_nodes(db),
        node_id=None,
        day_code=utils.get_currdate()
    )

@app.route('/online/statdata',apply=auth_opr,method=['GET','POST'])
def online_stat_data(db):    
    node_id = request.params.get('node_id')
    day_code = request.params.get('day_code')  
    opr_nodes = get_opr_nodes(db)
    if not day_code:
        day_code = utils.get_currdate()
    begin = datetime.datetime.strptime("%s 00:00:00"%day_code,"%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime("%s 23:59:59"%day_code,"%Y-%m-%d %H:%M:%S")
    begin_time,end_time = time.mktime(begin.timetuple()),time.mktime(end.timetuple())
    _query = db.query(models.SlcRadOnlineStat)
    
    if node_id:
        _query = _query.filter(models.SlcRadOnlineStat.node_id == node_id)
    else:
        _query = _query.filter(models.SlcRadOnlineStat.node_id.in_([i.id for i in opr_nodes]))
    
    _query = _query.filter(
        models.SlcRadOnlineStat.stat_time >= begin_time,
        models.SlcRadOnlineStat.stat_time <= end_time,
    )
    _data = [ (q.stat_time*1000,q.total) for q in _query ]
    return dict(code=0,data=[{'data':_data}])
        
permit.add_route("%s/online/stat"%__prefix__,u"在线用户统计",u"运维管理",is_menu=True,order=5)


@app.get('/flow/stat',apply=auth_opr)
def online_stat_query(db): 
    return render(
        "ops_flow_stat",
        node_list=get_opr_nodes(db),
        node_id=None,
        day_code=utils.get_currdate()
    )


@app.route('/flow/statdata',apply=auth_opr,method=['GET','POST'])
def flow_stat_data(db):    
    node_id = request.params.get('node_id')
    day_code = request.params.get('day_code')    
    opr_nodes = get_opr_nodes(db)
    if not day_code:
        day_code = utils.get_currdate()
    begin = datetime.datetime.strptime("%s 00:00:00"%day_code,"%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime("%s 23:59:59"%day_code,"%Y-%m-%d %H:%M:%S")
    begin_time,end_time = time.mktime(begin.timetuple()),time.mktime(end.timetuple())
    _query = db.query(models.SlcRadFlowStat)
    
    if node_id:
        _query = _query.filter(models.SlcRadFlowStat.node_id == node_id)
    else:
        _query = _query.filter(models.SlcRadFlowStat.node_id.in_([i.id for i in opr_nodes]))
    
    _query = _query.filter(
        models.SlcRadFlowStat.stat_time >= begin_time,
        models.SlcRadFlowStat.stat_time <= end_time,
    )
    
    in_data = {"name":u"上行流量","data":[]}
    out_data = {"name":u"下行流量","data":[]}
    
    for q in _query:
        _stat_time = q.stat_time * 1000
        in_data['data'].append([_stat_time,float(utils.kb2mb(q.input_total))])
        out_data['data'].append([_stat_time,float(utils.kb2mb(q.output_total))])

    return dict(code=0,data=[in_data,out_data])
        
permit.add_route("%s/flow/stat"%__prefix__,u"用户流量统计",u"运维管理",is_menu=True,order=5)        