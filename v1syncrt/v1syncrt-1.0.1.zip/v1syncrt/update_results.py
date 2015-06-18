__author__ = 'mjhunick'

from helpers import *
from v1pysdk import V1Meta
from configobj import ConfigObj
import argparse
import json
import ssl
import sys
from time import strftime


def update_regression_results(v1config, results, test_suite_id, test_set_id=None, v1=None):
    os.environ['OUTPUT'] = results_dir(v1config['yarara_base_dir'])  # Parametrize yarara functions

    if v1 is None:
        ssl._create_default_https_context = ssl._create_unverified_context  # TODO: ver si hay mejor forma
        v1 = V1Meta(instance_url=v1config['instance_url'], username=v1config['username'], password=v1config['password'])
    status_codes = v1config['status_codes']

    try:
        reg_suite = next(iter(v1.RegressionSuite.where(Number=test_suite_id)))
    except StopIteration:
        reg_suite = None
        assert 0, 'Suite does not exist in VersionOne'

    if test_set_id is None:
        # Create new test set
        assert 'test_set_prefix' in v1config, 'No test_set_prefix in config'
        prefix = v1config['test_set_prefix']
        v1.TestSet.select('Name')
        # current time and date
        current_time = strftime('%Y-%m-%dT%H:%M:%S')
        new_name = prefix + " " + current_time
        print 'Creating new test set: ' + new_name
        test_set = v1.TestSet.create(RegressionSuite=reg_suite, Name=new_name, Scope=reg_suite.SecurityScope)
        print 'Adding acceptance tests to test set'
        test_set.CopyAcceptanceTestsFromRegressionSuite()
    else:
        try:
            test_set = next(iter(v1.TestSet.where(Number=test_set_id)))
        except StopIteration:
            test_set = None
            assert 0, 'Test set does not exist in VersionOne'

    print 'Updating tests'
    for feature in results['features']:
        for scenario in feature['scenarios']:
            test_tags = filter(is_reg_test_number, scenario['tags'])
            if len(set(test_tags)) > 1:
                print 'Waring: More than one test tag for scenario ' + scenario['name']
                continue
            if not test_tags:
                continue
            tag = str(test_tags[0])
            status = str(scenario['status'])
            if status not in status_codes:
                continue
            try:
                test = [t for t in test_set.Children if t.GeneratedFrom.Number == tag][0]
                print 'Updating test ' + tag
                test.Status = v1.TestStatus(int(status_codes[status]))
                test.ActualResults = get_html_results(scenario)
            except IndexError:
                pass
    print 'Committing changes'
    v1.commit()


def main(argm=sys.argv, v1=None, v1config=None):
    if v1config is None:
        v1config = ConfigObj('versionone_config.cfg')
        v1config.setdefault('yarara_base_dir', '../../')

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
    if 'yarara_base_dir' in v1config:
        parser.add_argument('--yarara_dir', required=False, help='Base directory of Yarara project', default=v1config['yarara_base_dir'])
    else:
        parser.add_argument('--yarara_dir', required=True, help='Base directory of Yarara project')

    parser.add_argument('-tsu', '--test_suite_id', help='Number of VersionOne Regression Test Suite')
    parser.add_argument('-tse', '--test_set_id', nargs='?', help='Number of VersionOne Test Set', default=None)
    args = parser.parse_args(argm[1:])
    v1config['username'] = args.username
    v1config['password'] = args.password
    v1config['yarara_base_dir'] = args.yarara_dir

    if not is_reg_suite_number(args.test_suite_id):
        assert 0, 'Invalid test suite'
    if args.test_set_id and not is_test_set_number(args.test_set_id):
        assert 0, 'Invalid test set'

    for attr in ['instance_url', 'status_codes']:
        assert attr in v1config, ('Missing attribute %s on versionone_config.cfg' % attr)

    results = None
    try:
        with open(os.path.join(results_dir(v1config['yarara_base_dir']), 'test_results.json')) as f:
            results = json.load(f)
    except IOError:
        assert 0, 'Missing json results'
    except ValueError:
        assert 0, 'Malformed json results'

    update_regression_results(v1config, results, args.test_suite_id, args.test_set_id, v1)


if __name__ == '__main__':
    main()
