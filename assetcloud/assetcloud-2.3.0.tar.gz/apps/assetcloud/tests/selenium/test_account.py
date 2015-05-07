# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud.models import Account, get_user_profile_class
from selenium.common.exceptions import WebDriverException
from .utils import LoggedInSeleniumTestCase
from django.db import transaction
from selenium.common.exceptions import TimeoutException

UserProfile = get_user_profile_class()


class AccountUserSeleniumTests(LoggedInSeleniumTestCase):
    def get_tagged_with_radio(self):
        self.wait_for_display(value='tagged')
        return self.find_and_wait(value="tagged")

    def get_add_more_tags_input(self):
        self.wait_for_display(id="add_more_tags")
        return self.find_and_wait(id="add_more_tags")

    def add_tag(self, tag):
        self.get_tagged_with_radio().click()

        self.get_add_more_tags_input().send_keys(tag)

        self.find_and_wait(text_contains='Add Tag').click()

    def submit_form(self):
        self.find_and_wait(text_contains='Save').click()
        self.find_and_wait(css='.alert')

    def create_user(self):
        return UserProfile.create_account_user(
            account=self.selenium_user_account(),
            email='test@example.com',
            role=UserProfile.ROLE_EDITOR)

    def test_create_user(self):
        self.go_to_account_users()
        self.find_and_wait(link_text_contains='Add').click()

        self.find_and_wait(id="id_email").send_keys('test@example.com')
        self.add_tag('test')
        self.add_tag('test2')
        self.submit_form()
        self.assertDbUser(email='test@example.com', role='viewer',
                          tags=['test', 'test2'])
        self.find_and_wait(text_contains='Inactive')

    def test_create_user_shows_errors(self):
        self.create_user()
        self.go_to_account_users()
        self.find_and_wait(link_text_contains='Add').click()
        self.find_and_wait(id="id_email").send_keys('test@example.com')
        self.find_and_wait(id='id_save_user_button').click()
        try:
            self.find_and_wait(text_contains='This user already exists')
        except TimeoutException:
            self.fail('Should have found errors on form')

    def test_edit_user(self):
        user = self.create_user()
        self.go_to_account_users()
        self.find_and_wait(
            attribute_value=['data-user-id', str(user.pk)]).click()
        self.wait_for_display(id="viewer")
        self.find_and_wait(value='viewer').click()
        self.add_tag('test')
        self.submit_form()
        self.assertDbUser(email='test@example.com', role='viewer',
                          tags=['test'])

    def clicked_successfully(self, element):
        try:
            element.click()
            return True
        except WebDriverException:
            return False

    def test_autosave_tags(self):
        self.go_to_account_users()
        self.find_and_wait(link_text_contains='Add').click()

        self.find_and_wait(id="id_email").send_keys('autosave_test@example.com')
        self.get_tagged_with_radio().click()
        self.get_add_more_tags_input().send_keys('autosave, autosave2')
        self.submit_form()
        self.assertDbUser(email='autosave_test@example.com', role='viewer',
                          tags=['autosave', 'autosave2'])
        self.find_and_wait(text_contains='Inactive')

    def assertDbUser(self, email, role, tags=[]):
        try:
            profile = UserProfile.objects.get(user__email=email)
            user = profile.user
        except UserProfile.DoesNotExist:
            self.fail('User %s not in db' % email)
        else:
            self.assertEqual(user.email, email)
            self.assertEqual(profile.role, role)
            self.assertEqual(set(tags), {t.name for t in profile.visible_tags.all()})

    def go_to_account_users(self):
        self.find_and_wait(id='id_admin_menu_link').click()
        self.find_and_wait(link_text_contains='Users').click()


class CustomiseAccountSeleniumTests(LoggedInSeleniumTestCase):
    def test_add_homepage_tags(self):
        tags_to_add = {u'bear', u'hawk'}
        initial_tags = {u'rat', u'mouse'}

        final_tags = initial_tags | tags_to_add

        # Set initial tags in DB
        account = self.selenium_user_account()
        account.homepage_tags.add(*initial_tags)
        transaction.commit()

        # Add some more using the front end
        self.go_to_customise_account()

        for tag in tags_to_add:
            self.find_and_wait(id='add_more_tags').send_keys(tag)
            self.find_and_wait(id='id_add_tag_button').click()
            # wait for the click JavaScript to finish executing, otherwise
            # we might save the form before the tag is in the JSON hidden field
            self.find_and_wait(css='a.tag', link_text=tag)

        self.find_and_wait(id='save-customise').click()

        # Check correct tags are shown on page
        self.assert_tags_on_page_equal(final_tags)

        # Check correct tags are saved in DB
        self.assert_tags_in_db_equal(final_tags, account)

    def test_remove_homepage_tags(self):
        account = self.selenium_user_account()
        account.homepage_tags.add('moose', 'bison', 'gnu')
        transaction.commit()

        self.go_to_customise_account()

        self.find_and_wait(id='id_remove_tag_link_bison').click()
        self.find_and_wait(id='save-customise').click()

        self.assert_tags_on_page_equal({'moose', 'gnu'})
        self.assert_tags_in_db_equal({'moose', 'gnu'}, account)

    def go_to_customise_account(self):
        self.find_and_wait(id='id_admin_menu_link').click()
        self.find_and_wait(link_text_contains='Customise').click()

    def assert_tags_on_page_equal(self, expected_tag_names):
        page_tag_elements = self.find_and_wait(css='a.tag')
        page_tags = {element.text for element in page_tag_elements}
        self.assertEqual(expected_tag_names, page_tags)

    def assert_tags_in_db_equal(self, expected_tags, account):
        transaction.commit()
        reloaded_account = Account.objects.get(id=account.id)
        actual_tags = reloaded_account.homepage_tags.all()
        actual_tag_names = {tag.name for tag in actual_tags}
        self.assertEqual(expected_tags, actual_tag_names)
