'''
      _               _ _
   __| |_      _____ | | | __ _
  / _` \ \ /\ / / _ \| | |/ _` |
 | (_| |\ V  V / (_) | | | (_| |
  \__,_| \_/\_/ \___/|_|_|\__,_|

  An official requests based wrapper for the Dwolla API.

  This file contains functionality for all transactions related endpoints.
'''

from . import constants as c
from .rest import r


def send(destinationid, amount, params=False, alternate_token=False, alternate_pin=False):
    """
    Sends money to the specified destination user.

    :param destinationid: String of Dwolla ID to send funds to.
    :param amount: Double of amount to sen
    :param params: Dictionary of additional parameters
    :return: Integer of transaction ID
    """
    if not destinationid:
        raise Exception('send() requires destinationid parameter')
    if not amount:
        raise Exception('send() requires amount parameter')

    p = {
        'oauth_token': alternate_token if alternate_token else c.access_token,
        'pin': alternate_pin if alternate_pin else c.pin,
        'destinationId': destinationid,
        'amount': amount
    }

    if params:
        p = dict(list(p.items()) + list(params.items()))

    return r._post('/transactions/send', p)


def get(params=False, alternate_token=False):
    """
    Lists transactions for the user associated with
    the currently set OAuth token.

    :param params: Dictionary with additional parameters
    :return: Dictionary with transactions
    """
    p = {
        'oauth_token': alternate_token if alternate_token else c.access_token,
        'client_id': c.client_id,
        'client_secret': c.client_secret
    }

    if params:
        p = dict(list(p.items()) + list(params.items()))

    return r._get('/transactions', p)


def info(tid, alternate_token=False):
    """
    Returns transaction information for the transaction
    associated with the passed transaction ID

    :param id: String with transaction ID.
    :return: Dictionary with information about transaction.
    """
    if not tid:
        raise Exception('info() requires id parameter')

    return r._get('/transactions/' + tid,
                  {
                      'oauth_token': alternate_token if alternate_token else c.access_token,
                      'client_id': c.client_id,
                      'client_secret': c.client_secret
                  })


def refund(tid, fundingsource, amount, params=False, alternate_token=False, alternate_pin=False):
    """
    Refunds (either completely or partially) funds to
    the sending user for a transaction.

    :param id: String with transaction ID.
    :param fundingsource: String with funding source for refund transaction.
    :param amount: Double with amount to refun
    :param params: Dictionary with additional parameters.
    :return: Dictionary with information about refund transaction.
    """
    if not tid:
        raise Exception('refund() requires parameter id')
    if not fundingsource:
        raise Exception('refund() requires parameter fundingsource')
    if not amount:
        raise Exception('refund() requires parameter amount')

    p = {
        'oauth_token': alternate_token if alternate_token else c.access_token,
        'pin': alternate_pin if alternate_pin else c.pin,
        'fundsSource': fundingsource,
        'transactionId': tid,
        'amount': amount
    }

    if params:
        p = dict(list(p.items()) + list(params.items()))

    return r._post('/transactions/refund', p)


def stats(params=False, alternate_token=False):
    """
    Retrieves transaction statistics for
    the user associated with the current OAuth token.

    :param params: Dictionary with additional parameters
    :return: Dictionary with transaction statistics
    """
    p = {'oauth_token': alternate_token if alternate_token else c.access_token}

    if params:
        p = dict(list(p.items()) + list(params.items()))

    return r._get('/transactions/stats', p)

def schedule(destinationid, amount, scheduledate, fundssource, params=False, alternate_token=False, alternate_pin=False):
    """
    Sends money to the specified destination user.

    :param destinationid: String of Dwolla ID to send funds to.
    :param amount: Double of amount to sen
    :param scheduledate: YYYY-MM-DD format date for when to send funds.
    :param fundssource: Funding source ID to fund scheduled transaction
    :param params: Dictionary of additional parameters
    :return: Integer of transaction ID
    """
    if not destinationid:
        raise Exception('schedule() requires destinationid parameter')
    if not amount:
        raise Exception('schedule() requires amount parameter')
    if not scheduledate:
        raise Exception('schedule() requires scheduledate parameter')
    if not fundssource:
        raise Exception('schedule() requires fundssource parameter')

    p = {
        'oauth_token': alternate_token if alternate_token else c.access_token,
        'pin': alternate_pin if alternate_pin else c.pin,
        'destinationId': destinationid,
        'amount': amount,
        'scheduleDate': scheduledate,
        'fundsSource': fundssource
    }

    if params:
        p = dict(list(p.items()) + list(params.items()))

    return r._post('/transactions/scheduled', p)

def scheduled(params=False, alternate_token=False):
    """
    Retrieves all scheduled transactions

    :param params: Dictionary of additional parameters
    :return: List of scheduled transactions
    """
    p = {
        'oauth_token': alternate_token if alternate_token else c.access_token
    }

    if params:
        p = dict(list(p.items()) + list(params.items()))

    return r._get('/transactions/scheduled', p)

def scheduledbyid(tid, alternate_token=False):
    """
    Retrieve scheduled transaction by ID

    :param tid: Scheduled transaction ID
    :return: Requested scheduled transaction
    """
    if not tid:
        raise Exception('scheduledbyid() requires tid parameter')

    return r._get('/transactions/scheduled/' + tid, 
        {
            'oauth_token': alternate_token if alternate_token else c.access_token
        })

def editscheduledbyid(tid, params=False, alternate_token=False, alternate_pin=False):
    """
    Edit scheduled transaction by ID

    :param tid: Scheduled transaction ID
    :param params: Dictionary of additional parameters

    :return: Requested scheduled transaction
    """
    if not tid:
        raise Exception('editscheduledbyid() requires tid parameter')

    p = {
        'oauth_token': alternate_token if alternate_token else c.access_token,
        'pin': alternate_pin if alternate_pin else c.pin
    }

    if params:
        p = dict(list(p.items()) + list(params.items()))

    return r._put('/transactions/scheduled/' + tid, p)

def deletescheduledbyid(tid, alternate_token=False, alternate_pin=False):
    """
    Delete scheduled transaction by ID

    :param tid: Scheduled transaction ID
    :return: Requested scheduled transaction
    """
    if not tid:
        raise Exception('scheduledbyid() requires tid parameter')

    p = {
        'oauth_token': alternate_token if alternate_token else c.access_token,
        'pin': alternate_pin if alternate_pin else c.pin
    }

    return r._delete('/transactions/scheduled/' + tid, p)

def deleteallscheduled(alternate_token=False, alternate_pin=False):
    """
    Delete all scheduled transactions

    :return: Requested scheduled transaction
    """

    p = {
        'oauth_token': alternate_token if alternate_token else c.access_token,
        'pin': alternate_pin if alternate_pin else c.pin
    }

    return r._delete('/transactions/scheduled', p)