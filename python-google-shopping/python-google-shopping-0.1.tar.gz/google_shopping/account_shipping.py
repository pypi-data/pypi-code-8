from .mixins import ResourceMixin


class LocationGroup(object):
    pass


class AccountShipping(object):

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __repr__(self):
        return '<AccountShipping %s: %s>' % (
            self.id, self.title.encode('ascii', 'ignore')
        )


class AccountShippingManager(ResourceMixin):
    scope = 'accountshipping'
    resource_class = AccountShipping
    single_resource_id = 'productId'

    def get_sold_out(self):
        result = []
        products = self.list()
        for product in products:
            if product.is_out_of_stock:
                result.append(product)
        return result
