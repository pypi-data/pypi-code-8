from ..apibits import *
from .. import Client
from . import *

class Bank(APIResource):

    def remove(self, params={}, headers={}):
        params = ParamsBuilder.merge({
            "bank_id" : self.id,
        }, params)
        method = APIMethod("post", "/bank/delete", params, headers, self)
        json = self.client.execute(method)
        return json

    # Everything below here is used behind the scenes.
    def __init__(self, *args, **kwargs):
    	super(Bank, self).__init__(*args, **kwargs)
    	APIResource.register_api_subclass(self, "bank")

    _api_attributes = {
        "is_buyer_default" : {},
        "routing_number_string" : {},
        "account_number_string" : {},
        "is_active" : {},
        "bank_name" : {},
        "date" : {},
        "is_seller_default" : {},
        "nickname" : {},
        "account_class" : {},
        "account_type" : {},
        "name_on_account" : {},
        "resource_uri" : {},
        "id" : {},
        "is_verified" : {},
    }
