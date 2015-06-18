__author__ = 'glucero'

from helpers import *
from behave.parser import parse_file
from configobj import ConfigObj
from v1pysdk import V1Meta
import ssl
import argparse
import sys

def sync_tags(v1config, feature_paths, v1=None):
    if v1 is None:
        # Open version one sdk
        ssl._create_default_https_context = ssl._create_unverified_context  # TODO: ver si hay mejor forma
        v1 = V1Meta(instance_url=v1config['instance_url'], username=v1config['username'], password=v1config['password'])

    # Go through all the features file.
    for path in feature_paths:
        print 'Parsing feature ' + path
        feature = parse_file(path)

        # Go through all the scenarios in the feature file.
        for scenario in feature.scenarios:
            # Check if the scenario has tags.
            # If there is no tags do nothing.
            if len(set(scenario.tags)) == 0:
                continue

            # If there is a tag
            # Check if the scenario has regression test tag.
            reg_tags = filter(is_reg_test_number, scenario.tags)
            if len(set(reg_tags)) == 0:
                print 'The Scenario: "' + scenario.name + '" doesnt have a regression test tag.\n'
                continue

            if len(set(reg_tags)) > 1:
                print 'The Scenario: "' + scenario.name + '" has more than 1 regression test tag.\n'
                continue

            # Look for the regression test.
            try:
                test = next(iter(v1.RegressionTest.where(Number=reg_tags[0]).select('Tags')))
            # If the regression test doesnt exist
            except StopIteration:
                test = None
                print 'The Scenario: "' + scenario.name + '" has a regression test tag: "' \
                      + str(reg_tags[0]) + '" that doesnt exist in version one.\n'
                continue

            tags_to_add = scenario.tags
            tags_to_add.remove(reg_tags[0])

            if test.Tags is not None:
                tags_test = test.Tags.split()
            else:
                tags_test = []

            tags = set(tags_to_add + tags_test)
            tags = " ".join(tags)

            # Add tags to regression test.
            print 'Adding the tags: "' + str(tags) + '" to regression test: "' + str(test.Number) + '"'

            test.Tags = tags

    print 'Doing commit into version one.\n'
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

    args = parser.parse_args(argm[1:])
    v1config['username'] = args.username
    v1config['password'] = args.password
    v1config['yarara_base_dir'] = args.yarara_dir

    feature_paths = get_features_paths(feature_dir(v1config['yarara_base_dir']))

    if not feature_paths:
        assert 0, 'Could not find any feature file'

    sync_tags(v1config, feature_paths, v1)


if __name__ == '__main__':
    main()