from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from unittest import SkipTest

from metatags.models import URLMetatag
from metatags.tests.models import DummyModel1, DummyModel2

HOME_REGEX = "^" + reverse("home") + "$"


class AdminTestCase(TestCase):
    """ Test admin URLMetatag tag name choices.
    """

    @classmethod
    def setUpTestData(cls):
        super(AdminTestCase, cls).setUpTestData()
        cls.editor = get_user_model().objects.create(
            username="editor",
            email="editor@test.com",
            is_superuser=True,
            is_staff=True
        )
        cls.editor.set_password("password")
        cls.editor.save()


    def setUp(self):
        self.client.logout()

    def test_no_settings(self):
        self.client.login(username="editor", password="password")
        # No settings: default choices
        response = self.client.get("/admin/metatags/urlmetatag/add/")
        self.assertContains(response, """<option value="title">Title</option>""")
