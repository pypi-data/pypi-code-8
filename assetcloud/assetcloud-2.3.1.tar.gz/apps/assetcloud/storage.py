# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

import os.path
import storages.backends.s3boto
import uuid


class S3BotoStorage(storages.backends.s3boto.S3BotoStorage):
    """
    Variant of S3BotoStorage that makes sure that files with the same name
    don't overwrite each other.
    """

    def get_available_name(self, name):
        uniquifier = str(uuid.uuid4())

        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        # file_ext includes the dot.
        unique_name = os.path.join(dir_name, "%s_%s%s" % (file_root, uniquifier, file_ext))

        return super(S3BotoStorage, self).get_available_name(unique_name)
