from elasticsearch_dsl import field


class FileField(field.String):
    """handles serialization of a django.db.models.FileField to an Elasticsearch string field
    """

    def to_es(self, data):
        """handles the value mapping for djes

        :param data: the field's internals
        :type data: django.db.models.FileField

        :return: a string representation of the file path
        :rtype: str
        """
        return str(data)


class ImageField(FileField):
    """handles serialization of a django.db.models.ImageField to an Elasticsearch string field
    """

    def to_es(self, data):
        """handles the value mapping for djes

        :param data: the field's internals
        :type data: django.db.models.ImageField

        :return: a string representation of the file path
        :rtype: str
        """
        return str(data)
