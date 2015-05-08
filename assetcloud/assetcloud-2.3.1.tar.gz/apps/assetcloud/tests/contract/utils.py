import functools
from django.core.urlresolvers import reverse, NoReverseMatch
from django.template.base import Template, TemplateDoesNotExist
from django.template.context import Context
from django.template.loader import get_template
from assetcloud import random_utils
from django.test.testcases import TestCase
from assetcloud.asset_metadata_util import get_class_from_string


class ContractTestCase(TestCase):

    def assertBlockInTemplate(self, block_name, template_name):
        placeholder = random_utils.random_alphanumeric()
        template = Template("{% extends '" + template_name + "' %}{% block " + block_name + " %}{{ placeholder }}{% endblock %}")
        context = Context({"placeholder": placeholder})

        rendered_template = template.render(context=context)
        self.assertIn(placeholder, rendered_template, "Block %s does not exist in %s" % (block_name, template_name))

    def assertVariableInViewContext(self, variable_name, view_name):
        response = self.client.get(reverse(view_name))
        self.assertIn(variable_name, response.context, "Variable %s is not in view %s context" % (variable_name, view_name))

    def assertUrlExists(self, url_name):
        try:
            reverse(url_name)
        except NoReverseMatch:
            self.fail("URL named \"%s\" is used in an app but doesn't exist" % url_name)

    def assertValidImport(self, class_path):
        fail_message = "%s is used in imports but is not valid" % class_path
        try:
            get_class_from_string(class_path)
        except AttributeError:
            self.fail(fail_message)
        except ImportError:
            self.fail(fail_message)

    def assertTemplateExists(self, template_name):
        try:
            get_template(template_name)
        except TemplateDoesNotExist:
            self.fail("Template %s is used in an app but doesn't exist" % template_name)


class ContractTest(object):
    # Tests decorated with the ContractTest decorator need attention when being changed. Changes to make them pass may break contracts with other apps

    warning = "\n\n-- WARNING: --\n\nThis test is part of a contract with the app %s. Changing it to match your requirements will likely break %s as well."

    def __init__(self, app):
        self.app = app
        self.warning %= (app, app)

    def __call__(self, fn):
        @functools.wraps(fn)
        def decorated(*args, **kwargs):
            try:
                result = fn(*args, **kwargs)
            except AssertionError as e:
                raise AssertionError(e.message + self.warning)
            return result
        return decorated


TNABotContractTest = ContractTest(app="tnabot")
