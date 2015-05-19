from base64 import b64encode
import hashlib
from django.conf import settings

def make_external_transaction_id(transaction_id,
        fid=settings.TOUCHNET['accounting']['fau'],
        fau=settings.TOUCHNET['accounting']['fid']):
    return 'tID=%s FID=%sFAU=%s' % (transaction_id, fid, fau)

def get_transaction_id(external_transaction_id):
    return external_transaction_id.split()[0][4:]

def get_transaction_id_from_request(request):
    return get_transaction_id(request.GET['EXT_TRANS_ID'])

def make_validation_key(external_transaction_id, amount):
    msg = hashlib.md5()
    msg.update(settings.TOUCHNET['posting_key'])
    msg.update(external_transaction_id)
    msg.update(str(amount))
    return b64encode(msg.digest())
