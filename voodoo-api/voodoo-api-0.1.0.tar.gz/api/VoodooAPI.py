import json
import urllib
import urllib2

class VoodooAPI(object):
    #API_URL_BASE = "http://52.7.234.186:5001/api/0"
    API_URL_BASE = "http://localhost:5001/api/0"
    def __init__(self, api_key):
        self.api_key = api_key

    def api_post(self, path, body_values):
        headers = {
            "key": self.api_key,
            "content-type": "application/json"
        }
        url = VoodooAPI.API_URL_BASE + path
        data = json.dumps(body_values)

        request = urllib2.Request(url, data, headers)
        res = urllib2.urlopen(request)
        return json.loads(res.read())

    def api_get(self, path):
        headers = {
            "key": self.api_key
        }
        url = VoodooAPI.API_URL_BASE + path

        request = urllib2.Request(url, None, headers)
        res = urllib2.urlopen(request)
        return json.loads(res.read())

    def get_materials(self):
        return self.api_get('/materials');

    def createModel(self, file_url):
        values = {
            "file_url": file_url
        }
        return self.api_post('/model', values)

    def createOrder(self, order_items, shipping_info):
        values = {
            "order_items": order_items,
            "shipping_info": shipping_info
        }
        return self.api_post('/order/create', values)

    def confirmOrder(self, quote_id):
        values = {
            "quote_id": quote_id
        }
        return self.api_post('/order/confirm', values)

    def uploadAndOrderModel(self, file_url, qty, material, shipping_info):
        model = self.createModel(file_url)
        order_items = [{
            "id": model['id'],
            "qty": qty,
            "material": material
        }];

        order = self.createOrder(order_items, shipping_info)
        order_confirmation = self.confirmOrder(order["quote_id"])

        return order_confirmation

    def uploadAndQuoteModel(self, file_url, qty, material, shipping_info):
        model = self.createModel(file_url)
        order_items = [{
            "id": model['id'],
            "qty": qty,
            "material": material
        }]

        order = self.createOrder(order_items, shipping_info)
        return order
