try:
    from xmlrpc.client import DateTime
except ImportError:
    from xmlrpclib import DateTime


def package_list(options):
    return [{'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 287,
             'id': 1,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_std_1_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 279,
             'id': 2,
             'max_domains': 3,
             'min_domains': 1,
             'name': 'cert_std_3_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 289,
             'id': 3,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_std_w_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 1},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 24,
             'id': 4,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_1_10_0',
             'sgc': 0,
             'trustlogo': 1,
             'warranty': 10000,
             'wildcard': 0},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 34,
             'id': 5,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_1_100_0',
             'sgc': 0,
             'trustlogo': 1,
             'warranty': 100000,
             'wildcard': 0},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 317,
             'id': 6,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_1_100_SGC',
             'sgc': 1,
             'trustlogo': 1,
             'warranty': 100000,
             'wildcard': 0},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 7,
             'id': 7,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_1_250_0',
             'sgc': 0,
             'trustlogo': 1,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 35,
             'id': 8,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_w_250_0',
             'sgc': 0,
             'trustlogo': 1,
             'warranty': 250000,
             'wildcard': 1},
            {'category': {'id': 2, 'name': 'pro'},
             'comodo_id': 323,
             'id': 9,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_pro_w_250_SGC',
             'sgc': 1,
             'trustlogo': 1,
             'warranty': 250000,
             'wildcard': 1},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 337,
             'id': 10,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_bus_1_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 338,
             'id': 11,
             'max_domains': 1,
             'min_domains': 1,
             'name': 'cert_bus_1_250_SGC',
             'sgc': 1,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 279,
             'id': 12,
             'max_domains': 5,
             'min_domains': 1,
             'name': 'cert_std_5_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 279,
             'id': 13,
             'max_domains': 10,
             'min_domains': 1,
             'name': 'cert_std_10_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 1, 'name': 'standard'},
             'comodo_id': 279,
             'id': 14,
             'max_domains': 20,
             'min_domains': 1,
             'name': 'cert_std_20_0_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 0,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 410,
             'id': 15,
             'max_domains': 3,
             'min_domains': 1,
             'name': 'cert_bus_3_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 410,
             'id': 16,
             'max_domains': 5,
             'min_domains': 1,
             'name': 'cert_bus_5_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 410,
             'id': 17,
             'max_domains': 10,
             'min_domains': 1,
             'name': 'cert_bus_10_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0},
            {'category': {'id': 3, 'name': 'business'},
             'comodo_id': 410,
             'id': 18,
             'max_domains': 20,
             'min_domains': 1,
             'name': 'cert_bus_20_250_0',
             'sgc': 0,
             'trustlogo': 0,
             'warranty': 250000,
             'wildcard': 0
            }
           ]


def list(options):
    return [{'trustlogo': False,
             'assumed_name': None,
             'package': 'cert_std_1_0_0',
             'order_number': None,
             'altnames': [],
             'trustlogo_token': {'mydomain.name': 'adadadadad'},
             'date_incorporation': None,
             'card_pay_trustlogo': False,
             'contact': 'TEST1-GANDI',
             'date_start': None,
             'ida_email': None,
             'business_category': None,
             'cert': None,
             'date_end': None,
             'status': 'pending',
             'csr': '-----BEGIN CERTIFICATE REQUEST-----\n'
                    'MIICgzCCAWsCAQAwPjERMA8GA1UEAwwIZ2F1dnIuaX'
                    '...'
                    'K+I=\n-----END CERTIFICATE REQUEST-----',
             'date_updated': DateTime('20140904T14:06:26'),
             'software': 2,
             'id': 701,
             'joi_locality': None,
             'date_created': DateTime('20140904T14:06:26'),
             'cn': 'mydomain.name',
             'sha_version': 1,
             'middleman': '',
             'ida_tel': None,
             'ida_fax': None,
             'comodo_id': None,
             'joi_country': None,
             'joi_state': None},
            {'trustlogo': False,
             'assumed_name': None,
             'package': 'cert_bus_20_250_0',
             'order_number': None,
             'altnames': [],
             'trustlogo_token': {'inter.net': 'adadadadad'},
             'date_incorporation': None,
             'card_pay_trustlogo': False,
             'contact': 'TEST1-GANDI',
             'date_start': None,
             'ida_email': None,
             'business_category': None,
             'cert': None,
             'date_end': None,
             'status': 'valid',
             'csr': '-----BEGIN CERTIFICATE REQUEST-----\n'
                    'MIICgzCCAWsCAQAwPjERMA8GA1UEAwwIZ2F1dnIuaX'
                    '...'
                    'K+I=\n-----END CERTIFICATE REQUEST-----',
             'date_updated': DateTime('20140904T14:06:26'),
             'software': 2,
             'id': 706,
             'joi_locality': None,
             'date_created': DateTime('20140904T14:06:26'),
             'cn': 'inter.net',
             'sha_version': 1,
             'middleman': '',
             'ida_tel': None,
             'ida_fax': None,
             'comodo_id': None,
             'joi_country': None,
             'joi_state': None}
           ]


def info(id):
    cert = dict([(cert['id'], cert) for cert in list({})])
    return cert[id]


def create(*args):
    return {'id': 1}
