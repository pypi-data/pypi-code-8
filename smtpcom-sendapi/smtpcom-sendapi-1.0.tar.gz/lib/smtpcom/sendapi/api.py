from smtpcom.sendapi.send import SendAPI
from smtpcom.sendapi.report import ReportAPI
from smtpcom.sendapi.campaign import CampaignAPI
from smtpcom.sendapi.template import TemplateAPI

class API(object):

    def __init__(self, content_type='json'):
        self.__report = ReportAPI(content_type)
        self.__template = TemplateAPI(content_type)
        self.__campaign = CampaignAPI(content_type)
        self.__email = SendAPI(content_type)

    def create_campaign(self, *args, **kwargs):
        return self.__campaign.create_campaign(*args, **kwargs)

    def get_campaigns(self, *args, **kwargs):
        return self.__campaign.get_campaigns(*args, **kwargs)

    def add_template(self, *args, **kwargs):
        return self.__template.add_template(*args, **kwargs)

    def update_template(self, *args, **kwargs):
        return self.__template.update_template(*args, **kwargs)

    def delete_campaign(self, campaign_id):
        return self.__campaign.delete_campaign(campaign_id)

    def update_campaign(self, campaign_id, campaign_name):
        return self.__campaign.update_campaign(campaign_id, campaign_name)

    def delete_template(self, template_id):
        return self.__template.delete_template(template_id)

    def get_template(self, template_id):
        return self.__template.get_template(template_id)

    def get_templates(self, count, page):
        return self.__template.get_templates(count, page)

    def export_clicks(self, *args, **kwargs):
        return self.__report.export_clicks(*args, **kwargs)

    def export_clicks_by_url(self, *args, **kwargs):
        return self.__report.export_clicks_by_url(*args, **kwargs)

    def get_clicks_by_url(self, *args, **kwargs):
        return self.__report.get_clicks_by_url(*args, **kwargs)

    def export_opens(self, *args, **kwargs):
        return self.__report.export_opens(*args, **kwargs)

    def export_summary_stats(self, *args, **kwargs):
        return self.__report.export_summary_stats(*args, **kwargs)

    def get_clicks(self, *args, **kwargs):
        return self.__report.get_clicks(*args, **kwargs)

    def get_failed_sends(self, *args, **kwargs):
        return self.__report.get_failed_sends(*args, **kwargs)

    def get_opens(self, *args, **kwargs):
        return self.__report.get_opens(*args, **kwargs)

    def update_realtime_reporting(self, *args, **kwargs):
        return self.__report.update_realtime_reporting(*args, **kwargs)

    def get_realtime_reporting(self):
        return self.__report.get_realtime_reporting()

    def get_senders(self):
        return self.__report.get_senders()

    def get_sends(self, count, page):
        return self.__report.get_sends(count, page)

    def get_summary_stats(self, *args, **kwargs):
        return self.__report.get_summary_stats(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self.__email.send(*args, **kwargs)
