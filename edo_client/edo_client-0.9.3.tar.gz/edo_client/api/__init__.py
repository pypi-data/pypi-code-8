# -*- coding: utf-8 -*-
from .auth import AuthApi
from .org import OrgApi
from .oauth2 import OAuthApi
from .viewer import ViewerApi
from .operator import OperatorApi
from .content import ContentApi, ContentV2Api
from .message import MessageApi, MessageV2Api
from .session import SessionApi
from .package import PackageApi
from .admin import AdminApi
from account import AccountApi as account_api

class OperatorAPI:

    @property
    def operator(self):
        """ 当前用户相关的接口 """
        return OperatorApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

class OcAPI:

    @property
    def auth(self):
        """ 当前用户相关的接口 """
        return AuthApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

    @property
    def account(self):
        return account_api(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

    @property
    def oauth(self):
        """ 当前token相关的接口 """
        return OAuthApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

    @property
    def admin(self):
        """ 充值码相关接口, 易度内部使用 """
        return AdminApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)


class OrgAPI:

    @property
    def org(self):
        """ 组织架构相关的管理接口"""
        return OrgApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

class WoAPI:

    @property
    def content(self):
        return ContentApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

    @property
    def content_v2(self):
        return ContentV2Api(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)


    @property
    def workflows(self):
        return WorkflowApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

    @property
    def package(self):
        """ 当前用户相关的接口 """
        return PackageApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

class MessageAPI:

    @property
    def message(self):
        return MessageApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

    @property
    def message_v2(self):
        return MessageV2Api(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

    @property
    def session(self):
        return SessionApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)

class ViewerAPI:

    @property
    def viewer(self):
        return ViewerApi(self, self._access_token, self.refresh_hook, self.account_name, self.instance_name)
