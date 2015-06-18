__author__ = 'glucero'

from configobj import ConfigObj
from v1pysdk import V1Meta
import ssl
import sys
import argparse
from add_regression_test import main as main_regression_test
from add_to_suite import main as main_add_to_suite
from sync_tags import main as main_sync_tags
from sync_regression_suites_tags import main as main_sync_rs_tags
from update_results import main as main_update_results
from yarara.runner import run_scenarios
import os

def main(args_list=sys.argv[1:]):
    v1config = ConfigObj('versionone_config.cfg')
    v1config.setdefault('yarara_base_dir', '../')

    # Check if the username and password is in the parameters
    parser = argparse.ArgumentParser()
    if 'username' in v1config:
        parser.add_argument('-u', '--username', required=False, help='The username of VersionOne Client.', default=v1config['username'])
    else:
        parser.add_argument('-u', '--username', required=True, help='The username of VersionOne Client.')
    if 'password' in v1config:
        parser.add_argument('-p', '--password', required=False, help='The password of VersionOne Client.', default=v1config['password'])
    else:
        parser.add_argument('-p', '--password', required=True, help='The password of VersionOne Client.')

    parser.add_argument('--yarara_dir', required=False, help='Base directory of Yarara project', default=v1config['yarara_base_dir'])
    parser.add_argument('-ca', '--calls', required=True, nargs='+', help='Calls to do')

    args = parser.parse_args(args_list)

    common_args = [sys.argv[0], '-p', args.password, '-u', args.username, '--yarara_dir', args.yarara_dir]

    v1config['username'] = args.username
    v1config['password'] = args.password
    v1config['yarara_base_dir'] = args.yarara_dir

    print '\nVersionOne config: ' + str(v1config)
    for attr in ['instance_url']:
        assert attr in v1config, ('Missing attribute %s on versionone_config.cfg' % attr)

    # Open version one sdk
    ssl._create_default_https_context = ssl._create_unverified_context
    v1 = V1Meta(instance_url=v1config['instance_url'], username=v1config['username'], password=v1config['password'])

    for call_str in args.calls:
        print call_str
        try:
            if call_str == 'add_regression':
                main_regression_test(common_args, v1, v1config)
            elif call_str == 'add_to_suite':
                main_add_to_suite(common_args, v1, v1config)
            elif call_str == 'sync_tags':
                main_sync_tags(common_args, v1, v1config)
            elif call_str == 'sync_rs_tags':
                main_sync_rs_tags(common_args, v1, v1config)
            else:
                call = call_str.split()
                if call[0] == 'run_scenarios':
                    aux = sys.argv
                    sys.argv = call
                    aux_dir = os.getcwd()
                    os.chdir(os.path.join(v1config['yarara_base_dir'], 'project'))
                    run_scenarios(call[1:])
                    os.chdir(aux_dir)
                    sys.argv = aux
                elif call[0] == 'update_results':
                    args = call + common_args[1:]
                    main_update_results(args, v1, v1config)
                else:
                    print 'Unrecognized command: ' + call[0]
        except AssertionError as e:
            print 'Call "' + call_str + '" failed with message: ' + e.message
if __name__ == '__main__':
    main()