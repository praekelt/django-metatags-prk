from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase, override_settings
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
        if "test_no_settings" in settings.TEST_EXCLUDES:
            raise SkipTest()
        self.client.login(username="editor", password="password")
        # No settings: default choices
        response = self.client.get("/admin/metatags/urlmetatag/add/")
        self.assertContains(response, """<option value="title">Title</option>""")

    def test_include_settings(self):
        if "test_include_settings" in settings.TEST_EXCLUDES:
            raise SkipTest()
        self.client.login(username="editor", password="password")
        # We added a test tag and modified the title tag
        response = self.client.get("/admin/metatags/urlmetatag/add/")
        self.assertContains(response, """<option value="title">Modified Title</option>""")
        self.assertContains(response, """<option value="test_tag">Test Tag</option>""")

    def test_exclude_settings(self):
        if "test_exclude_settings" in settings.TEST_EXCLUDES:
            raise SkipTest()
        self.client.login(username="editor", password="password")
        # We added a test tag and removed the title tag
        response = self.client.get("/admin/metatags/urlmetatag/add/")
        self.assertNotContains(response, """<option value="title">""")
        self.assertContains(response, """<option value="test_tag">Test Tag</option>""")
