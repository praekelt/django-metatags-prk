from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import TestCase
from unittest import SkipTest

from metatags.models import URLMetatag
from metatags.tests.models import DummyModel1, DummyModel2

HOME_REGEX = "^" + reverse("home") + "$"


# TODO: If content has a title field, override
# TODO: Url pattern
# TODO: On object
# TODO: Extensibility of tag names


class AdminInlineTestCase(TestCase):
    """ Test admin inlines being added to content on the fly.

    Because the admin gets configured before any of the test override_settings
    decorators can run, we have to run this with different base settings and
    skip some of the tests if the settings are not the ones we expect.
    """

    @classmethod
    def setUpTestData(cls):
        super(AdminInlineTestCase, cls).setUpTestData()
        cls.editor = get_user_model().objects.create(
            username="editor",
            email="editor@test.com",
            is_superuser=True,
            is_staff=True
        )
        cls.editor.set_password("password")
        cls.editor.save()

        cls.model1 = DummyModel1.objects.create(title="Dummy Title 1")
        cls.model1.sites = Site.objects.all()
        cls.model1.save()

        cls.model2 = DummyModel2.objects.create(title="Dummy Title 2")
        cls.model2.sites = Site.objects.all()
        cls.model2.save()

    def setUp(self):
        self.client.logout()

    def test_no_settings(self):
        # Skip if we have any METATAGS settings
        if hasattr(settings, "METATAGS"):
            raise SkipTest()

        self.client.login(username="editor", password="password")
        # No settings: inlines should be on dummymodel1
        response = self.client.get("/admin/tests/dummymodel1/add/")
        self.assertContains(response, "<h2>Content metatags</h2>")
        # and on dummy model 2
        response = self.client.get("/admin/tests/dummymodel2/add/")
        self.assertContains(response, "<h2>Content metatags</h2>")
        # but NOT on urlmetatags. Those are always excluded
        response = self.client.get("/admin/metatags/urlmetatag/add/")
        self.assertNotContains(response, "<h2>Content metatags</h2>")

    def test_include_settings(self):
        # Skip if we don't have the correct settings
        if not hasattr(settings, "METATAGS") \
                or "inline_models" not in settings.METATAGS:
            raise SkipTest()

        self.client.login(username="editor", password="password")
        # No settings: inlines should be on dummymodel1
        response = self.client.get("/admin/tests/dummymodel1/add/")
        self.assertContains(response, "<h2>Content metatags</h2>")
        # and on dummy model 2
        response = self.client.get("/admin/tests/dummymodel2/add/")
        self.assertNotContains(response, "<h2>Content metatags</h2>")
        # but NOT on urlmetatags. Those are always excluded
        response = self.client.get("/admin/metatags/urlmetatag/add/")
        self.assertNotContains(response, "<h2>Content metatags</h2>")

    def test_exclude_settings(self):
        # Skip if we don't have the correct settings
        if not hasattr(settings, "METATAGS") \
                or "exclude_inline_models" not in settings.METATAGS:
            raise SkipTest()

        self.client.login(username="editor", password="password")
        # No settings: inlines should be on dummymodel1
        response = self.client.get("/admin/tests/dummymodel1/add/")
        self.assertContains(response, "<h2>Content metatags</h2>")
        # and on dummy model 2
        response = self.client.get("/admin/tests/dummymodel2/add/")
        self.assertNotContains(response, "<h2>Content metatags</h2>")
        # but NOT on urlmetatags. Those are always excluded
        response = self.client.get("/admin/metatags/urlmetatag/add/")
        self.assertNotContains(response, "<h2>Content metatags</h2>")

