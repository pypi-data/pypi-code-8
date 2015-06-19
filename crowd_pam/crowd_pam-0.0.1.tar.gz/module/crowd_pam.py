#!/usr/bin/env python
"""
Copyright @ 2015 Atlassian Pty Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys
from crowd_pam.getent import GetEnt
from crowd_pam.config import Config
from crowd_pam.error import ERROR as CROWD_ERROR
from crowd_pam.logs import get_logger
from crowd_pam.crowd_auth_utils import CrowdAuth as CrowdAuth

# Define some globals.  We will need them throughout
config = Config('/etc/crowd_pam.conf')
log = get_logger(config.logLevel)
log.debug("pam_sm_authenticate() starting")
crowd = CrowdAuth(
    app_url=config.crowd_url,
    app_name=config.crowd_application,
    app_pass=config.crowd_password,
    timeout=config.crowd_timeout,
    log=log
)
getent = GetEnt(log)


def pam_sm_authenticate(pamh, flags, argv):

    try:
        user = pamh.get_user(None)
        log.debug('crowd_pam::pam_sm_authenticate identified user: {}'.format(user))
    except pamh.exception, e:
        log.debug('crowd_pam encountered exception calling pam_get_user().  Exception: {}'.format(e))
        return e.pam_result

    if not user:
        log.warn("crowd_pam: failed to get user from pam_get_user()")
        return pamh.PAM_USER_UNKNOWN
    else:
        if crowd.verify_user(user):
            log.debug("crowd_pam: Pass: Creating local user account.")
            getent.createUser(user)
            getent.addUserToGroup(user, crowd.get_groups(user))
        else:
            log.warn("crowd_pam: Fail: User did not exist in crowd server.")
            return pamh.PAM_USER_UNKNOWN

    try:
        resp = pamh.conversation(pamh.Message(pamh.PAM_PROMPT_ECHO_OFF, "%s's Password: {}".format(user)))
        password = resp.resp
    except pamh.exception, e:
        log.debug("crowd_pam encountered exception getting password from user.  Exception: {}".format(e))
        return e.pam_result

    try:
        server_response = crowd.auth_user(user, password)
        log.debug("crowd_pam: web response received from crowd server.")
    except Exception, e:
        log.debug("crowd_pam encountered exception authenticating user.  Exception: {}".format(e))
        return pamh.PAM_SYSTEM_ERR

    try:
        if server_response is None:
            log.warn("crowd_pam: pam failed authentication due to error.")
            return pamh.PAM_SERVICE_ERR

        elif server_response == CROWD_ERROR.AUTHENTICATION_FAILED:
            log.warn("crowd_pam: user authentication failed for {}".format(user))
            return pamh.PAM_AUTH_ERR

        elif server_response == CROWD_ERROR.INVALID_USERNAME:
            log.warn("crowd_pam: invalid username contains illegal characters.  See IEEE Std 1003.1-2001")
            return pamh.PAM_SERVICE_ERR

        elif server_response == CROWD_ERROR.CROWD_CONNECT_FAILED:
            log.warn("crowd_pam: pam failed to connect to crowd server")
            return pamh.PAM_SERVICE_ERR

        elif server_response['active']:
            log.info("{} logged in".format(user))
            return pamh.PAM_SUCCESS
        else:
            log.info("Account expired for user {}".format(user))
            return pamh.PAM_ACCT_EXPIRED

    except Exception, e:
        log.warn('pam_sm_authenticate() Exception: {}'.format(e))
        return pamh.PAM_SYSTEM_ERR


def pam_sm_setcred(pamh, flags, argv):
    log.debug('pam_sm_setcred() invoked')
    return pamh.PAM_SUCCESS


def pam_sm_acct_mgmt(pamh, flags, argv):
    log.debug('pam_sm_acct_mgmt() invoked')
    return pamh.PAM_SUCCESS


def pam_sm_open_session(pamh, flags, argv):
    log.debug('pam_sm_open_session() invoked')
    return pamh.PAM_SUCCESS


def pam_sm_close_session(pamh, flags, argv):
    log.debug('pam_sm_close_session() invoked')
    return pamh.PAM_SUCCESS


def pam_sm_chauthtok(pamh, flags, argv):
    log.debug('pam_sm_chauthtok() invoked')
    return pamh.PAM_SUCCESS

if __name__ == '__main__':
    print crowd.verify_user(sys.argv[1])
