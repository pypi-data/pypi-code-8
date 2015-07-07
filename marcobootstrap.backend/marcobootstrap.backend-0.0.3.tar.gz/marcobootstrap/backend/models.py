from django.db import models

class Operation(models.Model):
    """
    Stores all the information related to an upcoming operation. This includes:
    - The operation type (reboot, update)
    - The operation time (as a float number with the number of seconds since the UNIX epoch)
    - A list of the hosts where the operation is going to be executed
    - The image of the OS to use in the upgrading process
    """
    operation_type=models.CharField(max_length=30, null=False)
    operation_time = models.FloatField(null=False)
    hosts = models.CharField(null=False, blank=False)
    image = models.CharField(max_length=50)

    class Meta:
        """
        A Django metaclass that helps in the interconnection with the SQL database
        It indicates the label of the application (so the model can exist in an atypical location, outside of models.py or a models package)
        and the database table where the model is to be stored
        """
        app_label = 'marco-bootstrap-backend'
        db_table = 'operation'

    def __unicode__(self):
        """
        Returns an unicode representation of the model
        """
        return self.operation_time + "--" + operation_type

class Configuration(models.Model):
    bootcode = models.CharField(max_length=60, null=False)

    class Meta:
        """
        A Django metaclass that helps in the interconnection with the SQL database
        It indicates the label of the application (so the model can exist in an atypical location, outside of models.py or a models package)
        and the database table where the model is to be stored
        """
        app_label = 'marco-bootstrap-backend'
        db_table = 'configuration'

    def __unicode__(self):
        """
        Returns an unicode representation of the model
        """
        return self.bootcode