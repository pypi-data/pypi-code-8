from smtpcom.sendapi import APIBase

class TemplateAPI(APIBase):

    @staticmethod
    def __prepare_params(html, subject, from_address, from_name, name):
        return {
            'Html': html,
            'Subject': subject,
            'From': from_address,
            'FromName': from_name,
            'TemplateName': name
        }

    def add_template(self, html, subject, from_address, from_name, name):
        data = self.__prepare_params(html, subject, from_address,
            from_name, name)
        return self.router.post(data, 'add_template')

    def update_template(self, html, subject, from_address, from_name,
            name, template_id):
        data = self.__prepare_params(html, subject, from_address,
            from_name, name)
        data['TemplateId'] = template_id
        return self.router.post(data, 'update_template')

    def delete_template(self, template_id):
        return self.router.post({'TemplateId': template_id},
            'delete_template')

    def get_template(self, template_id):
        return self.router.post({'TemplateId': template_id},
            'get_template')

    def get_templates(self, count, page):
        return self.router.post({'Count': count, 'Page': page},
            'get_templates')
