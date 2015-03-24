# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

from botocore.compat import six

from ..objects.exceptions import InvalidSyntaxError
from ..resources.strings import prompts

ENVIRONMENT_VAR_NAMESPACE = 'aws:elasticbeanstalk:application:environment'
CLOUDFORMATION_TEMPLATE = 'aws:cloudformation:template:parameter'
DATABASE_NAMESPACE = 'aws:rds:dbinstance'


def collect_changes(api_model, usr_model):
    """
    Grabs all things in the usr_model that are different and
   returns just the changes
    :param api_model: Model from api with Namespace keys
    :param usr_model: User model, key-value style
    :return: api_model
    """

    api_model = remove_unwanted_settings(api_model)
    ignore_default_resource_names(api_model)

    changes = []
    remove = []

    option_settings = api_model['OptionSettings']
    usr_options = usr_model['settings']
    for setting in option_settings:
        # Compare value for given optionName
        namespace = setting['Namespace']
        option = setting['OptionName']
        resource_name = None
        if 'ResourceName' in setting:
            resource_name = setting['ResourceName']
            key = resource_name + '.' + namespace
        else:
            key = namespace

        try:
            usr_value = usr_options[key][option]
            del usr_options[key][option]

            # If they dont match, take the user value
            if 'Value' in setting:
                if setting['Value'] != usr_value:
                    setting['Value'] = usr_value
                    if usr_value:
                        changes.append(setting)
                    else:
                        remove.append(
                            _get_option_setting_dict(namespace, option,
                                                     None, resource_name))
            else:
                if usr_value is not None:
                    setting['Value'] = usr_value
                    changes.append(setting)

        except KeyError:
            # user removed setting. We want to add to remove list
            d = _get_option_setting_dict(namespace, option,
                                         None, resource_name)
            remove.append(d)

    # Now we look for added options:
    for namespace, options in six.iteritems(usr_options):
        if options:
            namespace, resource_name = \
                _get_namespace_and_resource_name(namespace)
            for option, value in six.iteritems(options):
                changes.append(_get_option_setting_dict(namespace, option,
                                                        value, resource_name))

    return changes, remove


def _get_option_setting_dict(namespace, optionname, value, resource_name):
    d = {'Namespace': namespace, 'OptionName': optionname}
    if resource_name:
        d['ResourceName'] = resource_name
    if value:
        d['Value'] = value
    return d


def _get_namespace_and_resource_name(namespace):
    if '.' not in namespace:
        return namespace, None
    else:
        parts = namespace.split('.')
        if len(parts) > 2:
            raise InvalidSyntaxError(prompts['update.invalidsyntax'])
        return parts[1], parts[0]


def convert_api_to_usr_model(api_model):
    """
    Convert an api model with Namespaces to a User model as a key-value system
    Remove unwanted entries
    :param api_model:  Api model of environment
    :return: a user model
    """
    api_model = remove_unwanted_settings(api_model)
    ignore_default_resource_names(api_model)

    usr_model = dict()
    # Grab only data we care about
    _get_key('ApplicationName', usr_model, api_model)
    _get_key('EnvironmentName', usr_model, api_model)
    _get_key('DateUpdated', usr_model, api_model)
    usr_model['settings'] = dict()
    usr_model_settings = usr_model['settings']

    for setting in api_model['OptionSettings']:
        namespace = setting['Namespace']

        if 'ResourceName' in setting:
            namespace = setting['ResourceName'] + '.' + namespace
        if namespace not in usr_model_settings:
            #create it
            usr_model_settings[namespace] = dict()

        key = setting['OptionName']
        if 'Value' in setting:
            value = setting['Value']
        else:
            value = None

        usr_model_settings[namespace][key] = value

    return usr_model


def remove_unwanted_settings(api_model):
    option_settings = api_model['OptionSettings']
    api_model['OptionSettings'] = [
        setting for setting in option_settings if
            setting['Namespace'] != ENVIRONMENT_VAR_NAMESPACE and
            setting['Namespace'] != CLOUDFORMATION_TEMPLATE and
            not (setting['Namespace'] == DATABASE_NAMESPACE
                and (setting['OptionName'] == 'DBEngineVersion' or
                     setting['OptionName'] == 'DBUser' or
                     setting['OptionName'] == 'DBEngine' or
                     setting['OptionName'] == 'DBPassword'))

    ]
    return api_model


def ignore_default_resource_names(api_model):
    option_settings = api_model['OptionSettings']
    for setting in option_settings:
        if 'ResourceName' in setting and setting['ResourceName'] in \
            ['AWSEBAutoScalingGroup',
             'AWSEBAutoScalingLaunchConfiguration',
             'AWSEBEnvironmentName',
             'AWSEBLoadBalancer',
             'AWSEBRDSDatabase',
             'AWSEBSecurityGroup',
             ]:
            del setting['ResourceName']


def _get_key(KeyName, usr_model, api_model):
    usr_model[KeyName] = api_model[KeyName]