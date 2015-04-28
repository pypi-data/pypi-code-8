from django.db.models.base import Model
from django.db.models.fields import DateTimeField, TextField, EmailField


class PaymentLog(Model):

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'

    timestamp = DateTimeField(auto_now=True)
    data = TextField()
    email = EmailField(null=True)

    def __unicode__(self):
        return str(self.timestamp) + '-' + str(self.data) + '-' + str(self.email)