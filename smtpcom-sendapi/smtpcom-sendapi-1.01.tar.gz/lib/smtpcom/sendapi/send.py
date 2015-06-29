from smtpcom.sendapi import APIBase

class SendAPI(APIBase):

    def __init__(self, content_type='json'):
        super(SendAPI, self).__init__(content_type)

    def send(self, args):
        data = {
            'Subject': args.get('subject'),
            'BodyHtml': args.get('body_html'),
            'BodyText': args.get('body_text'),
            'TemplateID': args.get('template_id'),
            'From': args.get('from'),
            'FromName': args.get('from_name'),
            'ReplyTo': args.get('reply_to'),
            'ReplyToName': args.get('reply_to_name'),
            'ReturnPath': args.get('return_path'),
            'Recipients': args.get('recipients'),
            'RecipientsUrl': args.get('recipients_url'),
            'DefaultRecipientData': args.get('default_recipient_data'),
            'Attachments': args.get('attachments'),
            'Campaign': args.get('campaign_id'),
            'UTMCodes': args.get('utm_codes'),
            'EmailHeaders': args.get('email_headers')
        }
        return self.router.post(data, 'send')
