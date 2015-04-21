# -*- coding: utf-8 -*-
# http://wiki.open.weidian.com/index.php?title=%E9%A6%96%E9%A1%B5

import json
import urllib

import requests


class APIError(object):

    def __init__(self, code, msg):
        self.code = code
        self.message = msg


class VdianApi(object):

    API_PREFIX = 'https://api.vdian.com/'

    # 指定接口版本号
    API_VERSION = {
        'vdian.order.list.get': '1.1'
    }

    def __init__(self, appkey, secret, api_entry=None, access_token=None):
        self.appkey = appkey
        self.secret = secret
        self._access_token = access_token
        self.api_entry = api_entry or self.API_PREFIX
        self.api_method = api_entry or self.API_PREFIX + 'api'
        self.api_token = api_entry or self.API_PREFIX + 'token'

    @property
    def access_token(self):
        if not self._access_token:
            token, err = self.get_access_token()
            if not err:
                self._access_token = token['access_token']
                return self._access_token
            else:
                return None
        return self._access_token

    def set_access_token(self, token):
        self._access_token = token

    def get_access_token(self):
        params = {'grant_type': 'client_credential', 'appkey': self.appkey,
                  'secret': self.secret}
        resp = requests.get(
            self.api_token, params=params, verify=False, timeout=10,
        )
        return self._process_response(resp)

    def _process_response(self, resp):
        if resp.status_code != 200:
            return None, APIError(resp.status_code, 'http error')
        try:
            content = json.loads(resp.content)
        except:
            return None, APIError(99999, 'invalid rsp')
        if content['status']['status_code'] != 0:
            status = content['status']
            return None, APIError(
                status['status_code'], status['status_reason']
            )
        return content['result'], None

    def _get(self, method, param, api_v=None):
        public = {
            'method': method,
            'access_token': self._access_token,
            'format': 'json'}
        if api_v:
            public['version'] = api_v
        public = json.dumps(public)
        param = json.dumps(param)
        params = {'param': param, 'public': public}
        resp = requests.get(
            self.api_method, params=params, verify=False, timeout=10,
        )
        return self._process_response(resp)

    def get(self, method, param):
        return self._get(method, param, api_v=self.API_VERSION.get(method))

    def vdian_api(self, param, public):
        try:
            public = json.loads(public)
        except:
            raise 'json error'
        public['access_token'] = self._access_token,

        try:
            method = public['method']
        except:
            raise 'no method'

        if self.API_VERSION.get(method):
            public['version'] = self.API_VERSION[method]

        public = json.dumps(public)

        params = {'param': param, 'public': public}
        resp = requests.get(
            self.api_method, params=params, verify=False, timeout=10,
        )
        return resp

    def get_oauth_url(self, redirect_uri, state='123'):
        """ state 必须有东西, 不能为空字符串
        """
        url = self.api_entry + 'oauth2/authorize'
        oauth_url = ('{url}?appkey={appkey}&redirect_uri={redirect_uri}'
                     '&response_type=code&state={state}'.format(
                         url=url, appkey=self.appkey,
                         redirect_uri=urllib.quote(redirect_uri),
                         state=state
                     )
                     )

        return oauth_url

    def get_serve_access_token(self, code):
        """ 服务型应用获取token
        """
        params = {
            'appkey': self.appkey,
            'secret': self.secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        url = self.api_entry + 'oauth2/access_token'
        resp = requests.get(url, params=params, verify=False)
        return self._process_response(resp)

    def refresh_serve_access_token(self, refresh_token):
        params = {
            'appkey': self.appkey,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        url = self.api_entry + 'oauth2/refresh_token'
        print params
        resp = requests.get(url, params=params, verify=False)
        return self._process_response(resp)

    # sku字段说明
    # id 字符 sku唯一id
    # title 字符 sku名称
    # price 字符 价格
    # stock 整数 库存
    # sku_merchant_codes 字符 型号编码

    def vdian_item_get(self, itemid):
        """ 获取单个商品
            Args:
                itemid: 商品id
        """
        param = {'itemid': itemid}
        method = 'vdian.item.get'

        return self.get(method, param)

    def vdian_cps_item_get(self, itemid):
        """ 获取单个商品
            Args:
                itemid: 商品id
        """
        param = {'itemid': itemid}
        method = 'vdian.cps.item.get'

        return self.get(method, param)

    def vdian_item_list_get(
            self, shopid,
            page_num=1, page_size=30, orderby=1,
            update_start=None, update_end=None,):
        """ 获取微店的商品列表，进行商品管理，此接口不强制要求APPkey和店铺有绑定关系
        Args:
            page_num: 第几页, 首页从1开始
            page_size: 单页条数，默认值30，最大200
            orderby: 默认值1。
                            排序方式如下：
                            1---优先推荐
                            2---优先已售完(只返回已售完商品)
                            3---销量倒序
                            4---销量正序
                            5---库存倒序
                            6---库存正序

            update_start: 如: 2014-11-12 16:36:08
                商品更新时间段开始时间，精确到秒
            update_end: 如：2014-11-12 16:36:08
                商品更新时间段结束时间，精确到秒
            {u'item_num': 0, u'items': [], u'total_num': xx} 表示最后没有了
        """

        param = {
            'shopid': shopid, 'page_num': page_num,
            'page_size': page_size, 'orderby': orderby
        }
        if update_start:
            param['update_start'] = update_start
        if update_end:
            param['update_end'] = update_end
        method = 'vdian.item.list.get'

        return self.get(method, param)

    def vdian_item_add(
            self, item_name, imgs, price, stock, skus,
            merchant_code=None, fx_fee_rate=None, cate_ids=None):
        """ 创建微店商品
            Args:
                item_name:
                imgs: 数组, 商品图片url数组 第一张图片有效
                        商品图片地址通过“图片上传接口”获取
                price: 字符串 商品价格，如：'3.01' 输入范围：'0.01'-'99999999999.99'
                stock: 整数 库存
                merchant_code: 字符串 商品编码
                fx_fee_rate: 字符串 分销商分成比例
                cate_ids: 数组 商品分类id数组, 必须是店铺中已经存在的分类id
                skus: 数组 sku参数参见sku字段说明，无需上传id字段
                    [{"title":"型号1","price":"12","stock":"12","sku_merchant_code":"xh1"},]
                    规则：
                    title，必选，最多70个汉字
                    price，必选，输入范围0.01-99999999999.99
                    stock，必选，取值范围（0-999999999）
                    sku_merchant_code，可选，最长40个字
        """
        param = {
            'item_name': item_name,
            'imgs': imgs,
            'price': price,
            'stock': stock,
            'skus': skus
        }
        if merchant_code:
            param['merchant_code'] = merchant_code
        if fx_fee_rate:
            param['fx_fee_rate'] = fx_fee_rate
        if cate_ids:
            param['cate_ids'] = cate_ids
        method = 'vdian.item.add'

        return self.get(method, param)

    def vdian_item_update(
            self, itemid, price, stock, skus, item_name=None,
            merchant_code=None, fx_fee_rate=None, cate_ids=None):
        """ 创建微店商品
            Args:
                itemid:
                item_name:
                price: 字符串 商品价格，如：'3.01' 输入范围：'0.01'-'99999999999.99'
                stock: 整数 库存
                merchant_code: 字符串 商品编码
                fx_fee_rate: 字符串 分销商分成比例
                cate_ids: 数组 商品分类id数组, 必须是店铺中已经存在的分类id
                skus: 数组 sku参数参见sku字段说明，无需上传id字段
                    [{"title":"型号1","price":"12","stock":"12","sku_merchant_code":"xh1"},]
                    规则：
                    title，必选，最多70个汉字
                    price，必选，输入范围0.01-99999999999.99
                    stock，必选，取值范围（0-999999999）
                    sku_merchant_code，可选，最长40个字
        """
        param = {
            'itemid': itemid,
            'price': price,
            'stock': stock,
            'skus': skus
        }
        if item_name:
            param['item_name'] = item_name
        if merchant_code:
            param['merchant_code'] = merchant_code
        if fx_fee_rate:
            param['fx_fee_rate'] = fx_fee_rate
        if cate_ids:
            param['cate_ids'] = cate_ids
        method = 'vdian.item.update'

        return self.get(method, param)

    def vdian_item_sku_add(self, itemid, skus):
        """ 添加商品型号
            Args:
                itemid:
                skus: 数组 sku参数参见sku字段说明，更新sku，
                无需上传id字段
                [{"title":"1", "sku_merchant_code":"1",
                 "price":"1","stock":"1"}]
                title，可选，最多70个汉字
                price，可选，输入范围0.01-99999999999.99
                stock，可选，取值范围（0-999999999）
                sku_merchant_code，可选，最长40个字符,可以为空
        """
        param = {
            'itemid': itemid,
            'skus': skus
        }

        method = 'vdian.item.sku.add'

        return self.get(method, param)

    def vdian_item_ske_update(self, itemid, skus):
        """ 更新商品型号
            Args:
                itemid:
                skus: 数组 sku参数参见sku字段说明，更新sku，
                必须上传sku的id字段，
                [{"id":"1404259316","title":"1", "sku_merchant_code":"1",
                 "price":"1","stock":"1"}]
                id，必选，商品型号的ID
                title，可选，最多70个汉字
                price，可选，输入范围0.01-99999999999.99
                stock，可选，取值范围（0-999999999）
                sku_merchant_code，可选，最长40个字符,可以为空
        """
        param = {
            'itemid': itemid,
            'skus': skus
        }

        method = 'vdian.item.sku.update'

        return self.get(method, param)

    def vdian_item_image_add(self, itemid, imgs):
        """ 添加商品图片
            Args:
                itemid:
                imgs: 数组 图片url数组, 单个商品最多添加9张图片
        """
        param = {
            'itemid': itemid,
            'imgs': imgs
        }

        method = 'vdian.item.image.add'

        return self.get(method, param)

    def vdian_shop_cate_get(self, shopid):
        """ 获取商品分类
            Args:
                shopid:
        """
        param = {
            'shopid': shopid,
        }

        method = 'vdian.shop.cate.get'

        return self.get(method, param)

    def vdian_shop_cate_add(self, shopid, cates):
        """ 新增商品分类
            Args:
                shopid:
                cates: 分类对象 [{"cate_name":"上衣","sort_num":1},]
                cate_name: 字符串 输入范围[1-10个中文汉字]
                sort_num: 整数, 分类排序 选填
        """
        param = {
            'shopid': shopid,
            'cates': cates,
        }

        method = 'vdian.shop.cate.add'

        return self.get(method, param)

    def vdian_shop_cate_update(self, shopid, cates):
        """ 编辑商品分类
            Args:
                shopid:
                cates: 分类对象 [{"cate_name":"上衣","sort_num":1},]
                cate_name: 字符串 输入范围[1-10个中文汉字]
                sort_num: 整数, 分类排序 选填
                cate_id: 分类id
        """
        param = {
            'shopid': shopid,
            'cates': cates,
        }
        method = 'vdian.shop.cate.update'

        return self.get(method, param)

    def vdian_shop_cate_delete(self, shopid, cate_id):
        """ 删除商品分类
            Args:
                shopid:
                cate_id: 分类id
        """
        param = {
            'shopid': shopid,
            'cate_id': cate_id,
        }
        method = 'vdian.shop.cate.delete'

        return self.get(method, param)

    def vdian_item_cate_set(self, item_ids, cate_ids):
        """ 新增商品分类, 支持批量
            Args:
                shopid:
                item_ids: 商品id数组, 单次最多支持20个商品
                cate_ids: 分类id数组, 单次调用支持最多同时为20个微店商品设置20个分类
        """
        param = {
            'item_ids': item_ids,
            'cate_ids': cate_ids,
        }
        method = 'vdian.item.cate.set'

        return self.get(method, param)

    def vdian_item_cate_cancel(self, itemid, cate_ids):
        """ 取消商品分类
            Args:
                shopid:
                itemid: 商品id数组, 单次调用只能取消一个商品的分类
                cate_ids: 分类id数组, 单次支持同时取消最多20个分类
        """
        param = {
            'itemid': itemid,
            'cate_ids': cate_ids,
        }
        method = 'vdian.item.cate.cancel'

        return self.get(method, param)

    def vdian_order_list_get(
            self, page_num=1, page_size=30,
            order_type=None, add_start=None, add_end=None,
            update_start=None, update_end=None):
        """ 获取订单列表
            Args:
                order_type: 支持入参：
                    finish(完成的订单)
                    unpay (未付款订单)
                    pend (待处理订单)
                    close (关闭的订单)
                page_num: 订单翻页 初始页为1
                page_size: 单页条数
                add_start: 2014-11-12 16:36:08
                add_end: 2014-11-12 16:36:08
                update_start: 2014-11-12 16:36:08
                update_end: 2014-11-12 16:36:08
        """
        param = {
            'page_num': page_num,
            'page_size': page_size,
        }
        if order_type:
            param['order_type'] = order_type
        if add_start:
            param['add_start'] = add_start
        if add_end:
            param['add_end'] = add_end
        if update_start:
            param['update_start'] = update_start
        if update_end:
            param['update_end'] = update_end
        method = 'vdian.order.list.get'

        # 必须用 1.1
        return self.get(method, param, api_v='1.1')

    def vdian_order_get(self, order_id):
        """ 获取订单详情
        """
        param = {
            'order_id': order_id,
        }
        method = 'vdian.order.get'

        return self.get(method, param)

    def vdian_order_deliver(
            self, order_id, express_no, express_type,
            express_custom=None):
        """ 订单发货
            Args:
                express_type: 快递类型
                express_no: 快递单号
                支持快递类型:
                    1:顺丰速运，
                    2:圆通速递，
                    3:中通速递，
                    4:申通快递，
                    5:汇通快运，
                    6:韵达快递，
                    7:宅急送，
                    8:联邦快递，
                    9:EMS，
                    20:全峰快递，
                    21:百世汇通，
                    22:优速快递，
                    23:快捷快递，
                    24:德邦，
                    38248:国通快递，
                    42975:天天快递，
                    103032:马虎快递公司
                    999 为无需物流发货
                    业务规则：
                    当传express_type=0时，订单做自定义物流发货
                    则express_no必须传、不能为空
                    则express_custom必须传、不能为空
                    当传express_type等于以下数值时，订单做指定类型物流发货（
                    1:顺丰速运，2:圆通速递，3:中通速递，4:申通快递，5:汇通快运，
                    6:韵达快递，7:宅急送，8:联邦快递，9:EMS，20:全峰快递，
                    21:百世汇通，22:优速快递，23:快捷快递，24:德邦，38248:国通快递，
                    42975:天天快递，103032:马虎快递公司 ）
                    则express_no必须传、不能为空
                    则忽略express_custom入参
                    当传express_type=999 ，订单做无需物流发货
                    则忽略express_custom入参
                    则忽略express_no入参
                express_custom: 自定义快递，特殊可选
        """
        param = {
            'order_id': order_id,
            'express_type': express_type,
            'express_no': express_no,
        }
        if express_custom:
            param['express_custom'] = express_custom
        method = 'vdian.order.deliver'

        return self.get(method, param)

    def vdian_order_express_modify(
            self, order_id, express_no,
            express_type=None, express_custom=None):
        """ 修改物流信息
            Args:
                express_type: 快递类型
                express_no: 快递单号
                    如果只需修改单号，可只传express_no，不传express_type
                express_type:
                    当传express_type=0时，订单做自定义物流发货
                    则express_no必须传、不能为空
                    则express_custom必须传、不能为空
                    当传express_type等于以下数值时，订单做指定类型物流发货
                    【1:顺丰速运，2:圆通速递，3:中通速递，4:申通快递，5:汇通快运，l
                    6:韵达快递，7:宅急送，8:联邦快递，9:EMS，20:全峰快递，21:百世汇通，
                    22:优速快递，23:快捷快递，24:德邦，38248:国通快递，42975:天天快递，
                    103032:马虎快递公司 】
                    则express_no必须传、不能为空
                    则忽略express_custom入参
                    当传express_type=999 ，订单做无需物流发货
                    则忽略express_custom入参
                    则忽略express_no入参
                express_custom: 自定义快递，特殊可选
        """
        param = {
            'order_id': order_id,
            'express_no': express_no,
        }
        if express_custom:
            param['express_type'] = express_type
        if express_custom:
            param['express_custom'] = express_custom
        method = 'vdian.order.express.modify'

        return self.get(method, param)

    def vdian_order_modify(
            self, order_id, total_items_price, express_price):
        """ 修改订单价格
            Args:
                total_items_price: 修改订单的商品总价
                express_price: 修改订单运费价格
        """
        param = {
            'order_id': order_id,
            'total_items_price': total_items_price,
            'express_price': express_price,
        }

        method = 'vdian.order.modify'

        return self.get(method, param)

    def vdian_order_refund_accept(
            self, order_id, is_accept):
        """ 修改订单价格
            Args:
                is_accept: 只有传1时才会进行退款, 传0拒绝退款
        """
        param = {
            'order_id': order_id,
            'is_accept': is_accept,
        }

        method = 'vdian.order.refund.accept'

        return self.get(method, param)
