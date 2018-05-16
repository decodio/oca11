# Copyright 2017-2018 Simone Orsi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import exceptions
import mock

from .common import FormTestCase
from .fake_models import FakePublishModel, FakePublishModelForm


class TestFormPermCheck(FormTestCase):

    TEST_MODELS_KLASSES = [
        FakePublishModel,
        FakePublishModelForm,
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._setup_models()
        cls.record = cls.env[FakePublishModel._name].create({'name': 'Foo'})

    @classmethod
    def tearDownClass(cls):
        cls.record.unlink()
        cls._teardown_models()
        super().tearDownClass()

    mixin_path = 'odoo.addons.cms_info.models.website_mixin.WebsiteMixin'

    def test_form_check_permission_can_create(self):
        form = self.get_form(
            FakePublishModelForm._name, main_object=None)
        with mock.patch(self.mixin_path + '.cms_can_create') as patched:
            patched.return_value = True
            self.assertTrue(form.form_check_permission())
            patched.assert_called()

    def test_form_check_permission_cannot_create(self):
        form = self.get_form(
            FakePublishModelForm._name, main_object=None)
        with mock.patch(self.mixin_path + '.cms_can_create') as patched:
            patched.return_value = False
            try:
                form.form_check_permission()
            except exceptions.AccessError as err:
                patched.assert_called()
                msg = ('You are not allowed to create any record '
                       'for the model `%s`.') % FakePublishModel._name
                self.assertEqual(err.name, msg)

    def test_form_check_permission_can_edit(self):
        form = self.get_form(
            FakePublishModelForm._name,
            main_object=self.record)
        with mock.patch(self.mixin_path + '.cms_can_edit') as patched:
            patched.return_value = True
            self.assertTrue(form.form_check_permission())
            patched.assert_called()

    def test_form_check_permission_cannot_edit(self):
        form = self.get_form(
            FakePublishModelForm._name, main_object=self.record)
        with mock.patch(self.mixin_path + '.cms_can_edit') as patched:
            patched.return_value = False
            try:
                form.form_check_permission()
            except exceptions.AccessError as err:
                patched.assert_called()
                msg = (
                    'You cannot edit this record. Model: %s, ID: %d.'
                ) % (self.record._name, self.record.id)
                self.assertEqual(err.name, msg)
