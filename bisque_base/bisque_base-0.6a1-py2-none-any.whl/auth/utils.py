import logging
from bq.stores.common.tasks import update_document, query_documents

log = logging.getLogger("bq.bisque_auth")

class HashPassword():
    @staticmethod
    def create_password(password):
        if isinstance(password, unicode):
            password_8bit = password.encode('UTF-8')
        else:
            password_8bit = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update(password_8bit + salt.hexdigest())
        hashed_password = salt.hexdigest() + hash.hexdigest()
        return hashed_password

    @staticmethod
    def check_password(passval, password):
        hash = sha1()
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        hash.update(password + str(passval[:40]))
        return passval[40:] == hash.hexdigest()

class FreeTextPassword ():
    @staticmethod
    def create_password(password):
        return password
    @staticmethod
    def check_password(passval, password):
        return passval == password


password_map = {
    'hashed' : HashPassword,
    'freetext' : FreeTextPassword,
    }


def check_password (request, username=None, password=None):
    "Check the password for the current request"

    settings = request.registry.settings
    checker = password_map.get (settings.get ('bisque.login.password', 'freetext'))
    login_name = username #or request.unauthenticated_userid

    bqr = "SELECT ?p/@value_str as password WHERE { /_user:?u :/ tag:?p  FILTER ( ?u/@name = '%s' AND ?p/@name = 'password')}" % login_name

    #request = get_current_request()
    matches = query_documents (request, bqr)
    if matches:
        passval = matches[0]['password']
        if  checker.check_password ( passval, password):
            log.info ("Matched")
            return login_name
    return None


def new_login (request):
    login_name = request.authenticated_userid
    if not login_name:
        return
    bqr = "SELECT ?u/@resource_uniq as doc_id  WHERE { /user:?u  FILTER ( ?u/@name = '%s' ) }" % login_name
    matches =  query_documents (request, bqr)
    log.debug ("MD %s", matches)
    if matches:
        user_docid = matches[0]['doc_id']
        log.info ("USER_ID %s", user_docid)
        request.session['bisque.user.docid'] = user_docid


