"""
This is a formatter that outputs records in a key=value format.
"""

from .dict import DictFormatter

class KeyValFormatter(DictFormatter):
    """
    Note:
        This formatter will replace spaces with underscores in log record keys,
        and remove single quotes in record values.
    """
    def format(self, *args, **kwargs):
        msg_dict = super().format(*args, **kwargs)
        msg_str = ""
        for msg_key, msg_val in msg_dict.items(): 
            msg_key = str(msg_key)
            msg_val = str(msg_val)
            msg_key = msg_key.replace(" ", "_")
            msg_val = msg_val.replace("'", "")
            msg_str += "{0}='{1}' ".format(msg_key, msg_val)
        msg_str = msg_str.strip()
        return msg_str
