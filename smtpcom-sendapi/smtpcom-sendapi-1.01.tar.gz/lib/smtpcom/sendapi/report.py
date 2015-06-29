from smtpcom.sendapi import APIBase

class ReportAPI(APIBase):

    @staticmethod
    def __prepare_params(date_from, date_to, count,
            page, sender=None, campaign_id=None, url=None):
        data = {
            'DateFrom': date_from,
            'DateTo': date_to,
            'Count': count,
            'Page': page
        }
        if sender:
            data['Sender'] = sender
        if campaign_id:
            data['CampaignID'] = campaign_id
        if url:
            data['Url'] = url
        print 'Query Params: ', data
        return data

    def export_clicks(self, *args, **kwargs):
        params = self.__prepare_params(*args, **kwargs)
        data = self.router.post(params, 'export_clicks', raw_data=True)
        array = data.split('\n')[1:-2]
        if not array:
            return data
        return self.__csv_output("\n".join(array))

    def get_clicks(self, *args, **kwargs):
        params = self.__prepare_params(*args, **kwargs)
        data = self.router.post(params, 'get_clicks')
        return data

    def get_failed_sends(self, *args, **kwargs):
        params = self.__prepare_params(*args, **kwargs)
        data = self.router.post(params, 'get_failed_sends')
        return data

    def get_realtime_reporting(self):
        data = self.router.post({}, 'get_realtime_reporting')
        return data

    def get_senders(self):
        data = self.router.post({}, 'get_senders')
        return data

    def get_sends(self, count, page):
        data = self.router.post({'Count': count, 'Page': page}, 'get_sends')
        return data

    @staticmethod
    def __csv_output(data):
        array = data.split('\n')
        if not array:
            return data
        fields = array[0].lstrip('"').split(',')

        result = []
        for line in array[1:]:
            if not line:
                break
            item, values = {}, line.split(',')
            for i in range(len(fields)):
                item[fields[i]] = values[i]
            result.append(item)
        return result

    def export_clicks_by_url(self, *args, **kwargs):
        params = self.__prepare_params(*args, **kwargs)
        data = self.router.post(params, 'export_clicks_by_url', raw_data=True)
        return self.__csv_output(data)

    def get_clicks_by_url(self, *args, **kwargs):
        params = self.__prepare_params(*args, **kwargs)
        data = self.router.post(params, 'get_clicks_by_url', raw_data=True)
        return data

    def export_opens(self, *args, **kwargs):
        params = self.__prepare_params(*args, **kwargs)
        data = self.router.post(params, 'export_opens', raw_data=True)
        return self.__csv_output(data)

    def get_opens(self, *args, **kwargs):
        params = self.__prepare_params(*args, **kwargs)
        data = self.router.post(params, 'get_opens')
        return data

    @staticmethod
    def __prepare_summary_params(date_from, date_to,
            sender=None, campaign_id=None):
        params = {
            'DateFrom': date_from,
            'DateTo': date_to,
        }
        if sender:
            params['Sender'] = sender
        if campaign_id:
            params['CampaignID'] = campaign_id
        return params

    def export_summary_stats(self, *args, **kwargs):
        params = self.__prepare_summary_params(*args, **kwargs)
        data = self.router.post(params, 'export_summary_stats', raw_data=True)
        return self.__csv_output(data)

    def get_summary_stats(self, *args, **kwargs):
        params = self.__prepare_summary_params(*args, **kwargs)
        return self.router.post(params, 'get_summary_stats')

    def update_realtime_reporting(self, queue_name, server_region, public_key,
            private_key, notify_opens, notify_clicks, notify_delivery_info):
        params = {
            'QueueName': queue_name,
            'ServerRegion': server_region,
            'PublicAccessKey': public_key,
            'PrivateAccessKey': private_key,
            'NotifyOpens': notify_opens,
            'NotifyClicks': notify_clicks,
            'NotifyDelivertInfo': notify_delivery_info
        }
        return self.router.post(params, 'update_realtime_reporting')
