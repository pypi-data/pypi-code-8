# -*- coding: UTF-8 -*-
# lvjiyong on 2015/6/3.

import logging
import os


_log_config = os.path.join(os.path.dirname(__file__), '..\\data\\logging.conf')
if os.path.exists(_log_config):
    import logging.config
    logging.config.fileConfig(_log_config)
else:
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filemode='w')
logger = logging.getLogger('gelid')