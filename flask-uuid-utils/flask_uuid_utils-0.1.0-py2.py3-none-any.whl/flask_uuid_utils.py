__version__ = '0.1.0'


from datetime import datetime
from os import path
from binascii import unhexlify
import uuid
from werkzeug import secure_filename


def generate_binary_uuid():
    return uuid_to_binary(str(uuid.uuid4()))


def uuid_to_binary(uuid_hex_hyphened):
    return unhexlify(uuid_hex_hyphened.replace('-', ''))


def prefix_file_uuid(obj, file_data):
    parts = path.splitext(file_data.filename)
    return secure_filename('%s%s' % (obj.uuid_hex_hyphened, parts[1]))


def prefix_file_uuid_utcnow(obj, file_data):
    parts = path.splitext(file_data.filename)
    return secure_filename('%s-%s%s' % (obj.uuid_hex_hyphened, datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S'), parts[1]))

