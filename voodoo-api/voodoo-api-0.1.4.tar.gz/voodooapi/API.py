import json
import urllib
import urllib2

class API(object):
    API_URL_BASE = "https://api.voodoomfg.co/api/0"
    def __init__(self, api_key):
        self.api_key = api_key

    def api_post(self, path, body_values):
        headers = {
            "key": self.api_key,
            "content-type": "application/json"
        }
        url = API.API_URL_BASE + path
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

    def create_model(self, file_url):
        values = {
            "file_url": file_url
        }
        return self.api_post('/model', values)

    def create_order(self, order_items, shipping_info):
        values = {
            "order_items": order_items,
            "shipping_info": shipping_info
        }
        return self.api_post('/order/create', values)

    def confirm_order(self, quote_id):
        values = {
            "quote_id": quote_id
        }
        return self.api_post('/order/confirm', values)

    def upload_and_order_model(self, file_url, qty, material, shipping_info):
        model = self.create_model(file_url)
        order_items = [{
            "id": model['id'],
            "qty": qty,
            "material": material
        }];

        order = self.create_order(order_items, shipping_info)
        order_confirmation = self.confirm_order(order["quote_id"])
        return order_confirmation

    def upload_and_quote_model(self, file_url, qty, material, shipping_info):
        model = self.create_model(file_url)
        order_items = [{
            "id": model['id'],
            "qty": qty,
            "material": material
        }]

        order = self.create_order(order_items, shipping_info)
        return order
