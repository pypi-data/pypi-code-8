from django import template
from django.conf import settings

from grappelli.dashboard.utils import _get_dashboard_cls

register = template.Library()


@register.tag
def get_left_dashboard(parser, token):
    """{% get_left_dashboard %}"""
    return GetLeftDashboardNode()


class GetLeftDashboardNode(template.Node):

    def render(self, context):
        dashboard = _get_dashboard_cls(getattr(
            settings,
            "CMS_LEFT_DASHBOARD",
            "interim_cms.dashboard.LeftDashboard"
        ), context)()
        context["left_dashboard"] = dashboard
        return ""


@register.tag
def get_center_dashboard(parser, token):
    """{% get_center_dashboard %}"""
    return GetCenterDashboardNode()


class GetCenterDashboardNode(template.Node):

    def render(self, context):
        dashboard = _get_dashboard_cls(getattr(
            settings,
            "CMS_CENTER_DASHBOARD",
            "interim_cms.dashboard.CenterDashboard"
        ), context)()
        context["center_dashboard"] = dashboard
        return ""


@register.tag
def get_right_dashboard(parser, token):
    """{% get_right_dashboard %}"""
    return GetRightDashboardNode()


class GetRightDashboardNode(template.Node):

    def render(self, context):
        dashboard = _get_dashboard_cls(getattr(
            settings,
            "CMS_RIGHT_DASHBOARD",
            "interim_cms.dashboard.RightDashboard"
        ), context)()
        context["right_dashboard"] = dashboard
        return ""
