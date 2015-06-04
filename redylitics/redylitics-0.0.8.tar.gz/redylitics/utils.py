#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import logging
from logging import handlers
import os


LOGGER = logging.getLogger("redylitics")
LOGGER.setLevel(logging.INFO)
log_file_name = os.environ.get("REDYLITICS_LOG_FILE_NAME", "redylitics.log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = handlers.RotatingFileHandler(log_file_name, maxBytes=5000000, backupCount=5)
handler.setFormatter(formatter)
LOGGER.addHandler(handler)


GIF = base64.b64decode("R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==")
