from django.db import models


class MailgunSettings(models.Model):
    key = models.CharField(max_length=255, blank=False, null=False, unique=True)
    value = models.CharField(max_length=255, blank=False, null=False)

    def __str__(self):
        return "Mailgun ({key}): {value}".format(key=self.key, value=self.value)
