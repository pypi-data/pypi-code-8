__author__ = 'glucero'

from helpers import *
from configobj import ConfigObj
from v1pysdk import V1Meta
import ssl
import sys
import argparse


def sync_regression_test(v1config, feature_paths, v1=None):
    if v1 is None:
        # Open version one sdk
        ssl._create_default_https_context = ssl._create_unverified_context  # TODO: ver si hay mejor forma
        v1 = V1Meta(instance_url=v1config['instance_url'], username=v1config['username'], password=v1config['password'])

# Look for the scope of the project.
    try:
        scope = next(iter(v1.Scope.where(Name=v1config['project'])))
    # If the project name doesnt exits its an error.
    except StopIteration:
        scope = None
        assert 0, 'There is no Scope with name: ' + v1config['project']

    # Go through all the features file.
    for path in feature_paths:
        print 'Parsing feature ' + path
        feature = FeatureWrapper(path)

        # Go through all the scenarios in the feature file.
        for scenario in feature.scenarios:
            # Check if the scenario has the tag to add to version one
            if v1config["tag_to_add_regression"] in scenario.tags:
                # If the Scenario also has a tag of a regression test its an error.
                reg_tags = filter(is_reg_test_number, scenario.tags)
                if len(set(reg_tags)) != 0:
                    print 'Warning: The Scenario "' + scenario.name + '" has a tag of a regression' \
                                                            ' test and the tag: ' + v1config["tag_to_add_regression"]
                    continue

                new_name = scenario.name
                steps = scenario.steps
                setup = scenario.background.steps
                steps = escape_html(steps_to_string(steps))
                setup = escape_html(steps_to_string(setup))

                tags = " ".join(t for t in scenario.tags if t != v1config["tag_to_add_regression"])

                # Create the regression test.
                regression_test = v1.RegressionTest.create(Name=new_name, Scope=scope,
                                                            Steps=steps, Setup=setup, Tags=tags)
                # Tag to put in scenario
                tag = regression_test.Number
                print "\n Regression test: " + tag + " created.\n"

                # Change the tag "tag_to_add_regression" for the tag of the regression test.
                scenario.add_tag(tag)
                scenario.remove_tag(v1config["tag_to_add_regression"])

        feature.dump_to_file()


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

    sync_regression_test(v1config, feature_paths, v1)


if __name__ == '__main__':
    main()
