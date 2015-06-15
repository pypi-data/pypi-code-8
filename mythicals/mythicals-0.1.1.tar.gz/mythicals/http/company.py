import inspect

import sqlalchemy.orm as saorm

from mythicals import form, domain, config

from . import request, DB, Resource, Id, exc


class AuthorizeMixin(object):

    def authorize(self, target, action, *nesting):
        if target is None:
            self._authorize_none(action, *nesting)
        elif inspect.isclass(target) and issubclass(target, Resource):
            self._authorize_type(target, action, *nesting)
        elif isinstance(target, Resource):
            self._authorize_instance(target, action, *nesting)
        else:
            raise NotImplementedError

    def _authorize_none(self, action, *nesting):
        raise NotImplementedError

    def _authorize_type(self, resource_cls, action, *nesting):
        raise NotImplementedError

    def _authorize_instance(self, resource, action, *nesting):
        raise NotImplementedError



class Company(Resource, AuthorizeMixin):

    id = Id(prefix='COP')

    name = form.String()

    created_at = form.DateTime()

    updated_at = form.DateTime()

    @classmethod
    def authenticate(cls, name, password):
        try:
            obj = domain.Company.query.filter_by(name=name).one()
        except saorm.exc.NoResultFound:
            return
        if not obj.authenticate(password):
            return
        return cls(obj)

    @property
    def credit_card_ops(self):
        return self.obj.credit_card_ops

    @property
    def credit_card_submissions(self):
        return self.obj.credit_card_submissions

    @property
    def bank_account_ops(self):
        return self.obj.bank_account_ops

    @property
    def bank_account_submissions(self):
        return self.obj.bank_account_submissions

    @property
    def merchant_ops(self):
        return self.obj.merchant_ops

    @property
    def merchant_submissions(self):
        return self.obj.merchant_submissions

    # AuthorizeMixin

    def _authorize_none(self, action, *nesting):
        pass

    def _authorize_type(self, resource_cls, action, *nesting):
        for resource in nesting:
            if hasattr(resource, 'company') and resource.comany != self:
                raise exc.Forbidden()

    def _authorize_instance(self, resource, action, *nesting):
        if hasattr(resource, 'company') and resource.company != self:
            raise exc.Forbidden()
        for resource in nesting:
            if hasattr(resource, 'company') and resource.comany != self:
                raise exc.Forbidden()


Company.bind(DB(domain.Company))


class Anonymous(Resource, AuthorizeMixin):

    def _authorize_none(self, action, *nesting):
        if action not in ('health', 'boom'):
            raise exc.Unauthorized()
        if not any(
               request.remote_ip_addr in cidr
               for cidr in config.API_ALLOWED_CIDRS
            ):
            raise exc.Unauthorized()

    def _authorize_type(self, resource_cls, action, *nesting):
        raise exc.Unauthorized()

    def _authorize_instance(self, resource, action, *nesting):
        raise exc.Unauthorized()
