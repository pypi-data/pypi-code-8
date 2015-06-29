from smtpcom.sendapi import APIBase

class CampaignAPI(APIBase):

    def create_campaign(self, campaign_name, campaign_id=None):
        if not campaign_name:
            raise ValueError("Campaign name should not be blank")
        data = {'CampaignName': campaign_name}
        if campaign_id:
            data['CampaignId'] = campaign_id
        return self.router.post(data, 'create_campaign')

    def delete_campaign(self, campaign_id):
        return self.router.post({'CampaignId': campaign_id},
            'delete_campaign')

    def get_campaigns(self, sender, count, page):
        return self.router.post({'Sender': sender, 'Count': count,
            'Page': page}, 'get_campaigns')

    def update_campaign(self, campaign_id, campaign_name):
        return self.router.post({'CampaignId': campaign_id,
            'CampaignName': campaign_name}, 'update_campaign')
