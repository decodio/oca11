# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo.addons.cms_form.tests.common import FormTestCase
from odoo.addons.cms_form.tests.utils import fake_request
from .fake_models import FakePartnerOverride
import mock


class TestAccountForm(FormTestCase):

    TEST_MODELS_KLASSES = [FakePartnerOverride]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_models()
        cls.user_model = cls.env['res.users'].with_context(
            no_reset_password=True, tracking_disable=True)
        cls.user1 = cls.user_model.create({
            'name': 'Test User 1',
            'login': 'testuser1',
            'email': 'testuser1@email.com',
            # make sure to have only portal group
            'groups_id': [(6, 0, [cls.env.ref('base.group_portal').id])]
        })
        cls.partner1 = cls.user1.partner_id

    @classmethod
    def tearDownClass(cls):
        cls._teardown_models()
        super().tearDownClass()

    def test_form_update(self):
        self.assertEqual(self.partner1.name, 'Test User 1')
        data = {
            'name': 'Edward Norton',
        }
        request = fake_request(form_data=data, method='POST')
        # get the form to edit partner1
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            req=request,
            main_object=self.partner1)
        # submit form as user1
        form.form_create_or_update()
        self.assertEqual(self.partner1.name, data['name'])

    def test_form_update_email_validation_called(self):
        data = {
            'email': 'this email is #so_wrong',
        }
        request = fake_request(form_data=data, method='POST')
        # get the form to edit partner1
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            req=request,
            main_object=self.partner1)
        patch_path = \
            'odoo.addons.cms_account_form.models.account_form.AccountForm'
        with mock.patch(patch_path + '._form_validate_email') as patched:
            # method is mocked thus is going to return a mocked object
            # instead of a tuple. `form_validate` will raise ValueError
            patched.return_value = ('email_not_valid', 'message')
            form.form_process()
            patched.assert_called_with(
                'this email is #so_wrong',
                # request values
                email='this email is #so_wrong',
            )

    def test_form_update_vat_validation_called(self):
        data = {
            'vat': 'this VAT is #so_wrong',
        }
        request = fake_request(form_data=data, method='POST')
        # get the form to edit partner1
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            req=request,
            main_object=self.partner1)
        patch_path = \
            'odoo.addons.cms_account_form.models.account_form.AccountForm'
        with mock.patch(patch_path + '._form_validate_vat') as patched:
            # method is mocked thus is going to return a mocked object
            # instead of a tuple. `form_validate` will raise ValueError
            patched.return_value = ('vat_not_valid', 'message')
            form.form_process()
            patched.assert_called_with(
                'this VAT is #so_wrong',
                # request values
                vat='this VAT is #so_wrong',
            )

    def test_validate_vat_ok(self):
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            ctx={'test_do_fail': False},
            main_object=self.partner1)
        error, msg = form._form_validate_vat('THIS_VAT_IS_OK ;)')
        self.assertEqual(error, None)
        self.assertEqual(msg, None)

    def test_validate_vat_fail(self):
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            ctx={'test_do_fail': True},
            main_object=self.partner1)
        error, msg = form._form_validate_vat('000000000')
        self.assertEqual(error, 'vat_not_valid')
        self.assertEqual(msg, 'VAT check failed')

    def test_validate_email_ok(self):
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            main_object=self.partner1)
        error, msg = form._form_validate_email('john.doe@notsorealemail.com')
        self.assertEqual(error, None)
        self.assertEqual(msg, None)

    def test_validate_email_fail(self):
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            main_object=self.partner1)
        error, msg = form._form_validate_email('john.doe+notsorealemail.com')
        self.assertEqual(error, 'email_not_valid')
        self.assertEqual(
            msg, 'Invalid Email! Please enter a valid email address.')

    # Mock status message because it needs a real website session
    # and we don't need it now.
    @mock.patch('odoo.addons.cms_status_message.models.website'
                '.Website.add_status_message')
    def test_update_email_exists(self, mocked_add_status_msg):
        self.user_model.create({
            'name': 'Lock a new email',
            'login': 'lockit',
            'email': 'lockit@email.com',
        })
        data = {
            'email': 'lockit@email.com',
        }
        request = fake_request(form_data=data, method='POST')
        # get the form to edit partner1
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            req=request,
            main_object=self.partner1)
        # make status message machinery happy
        form.o_request.website = self.env['website'].browse(1)
        result = form._handle_email_update(self.user1, data)
        # no update happened
        self.assertFalse(result)
        # and we got a nice status message
        msg = 'Email address `lockit@email.com` already taken.'
        self.assertEqual(mocked_add_status_msg.call_args[0][0], msg)

    @mock.patch('odoo.addons.cms_status_message.models.website'
                '.Website.add_status_message')
    @mock.patch('odoo.addons.auth_signup.models.res_users'
                '.ResUsers.reset_password')
    def test_update_email_ok(self, mocked_reset_pwd, mocked_add_status_msg):
        data = {
            'email': 'new@email.com',
        }
        request = fake_request(form_data=data, method='POST')
        # get the form to edit partner1
        form = self.get_form(
            'cms.form.my.account',
            sudo_uid=self.user1.id,
            req=request,
            main_object=self.partner1)

        # # make status message machinery happy
        form.o_request.website = self.env['website'].browse(1)

        result = form._handle_email_update(self.user1, data)
        # email has been updated
        self.assertEqual(self.partner1.email, data['email'])
        # use login too
        self.assertEqual(self.user1.login, data['email'])
        # result is ok
        self.assertTrue(result)
        # user has been logged out
        self.assertTrue(form.o_request.session.test_logged_out)
        # password reset has been forced
        mocked_reset_pwd.assert_called()

        # and we got a nice status message
        msg = ('Your login username has changed to: `new@email.com`. '
               'An email has been sent to verify it. '
               'You will be asked to reset your password.')
        self.assertEqual(mocked_add_status_msg.call_args[0][0], msg)
