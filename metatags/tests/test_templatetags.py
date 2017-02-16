from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test import TestCase

from metatags.models import URLMetatag

HOME_REGEX = "^" + reverse("home") + "$"


# TODO: If content has a title field, override
# TODO: Url pattern
# TODO: On object
# TODO: Extensibility of tag names


class TemplateTagsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsTestCase, cls).setUpTestData()
        cls.tag = URLMetatag.objects.create(name="keywords", content="testa,testb", url="^/$")
        cls.tag.sites = Site.objects.all()
        cls.tag.save()

    def test_default_tags(self):
        response = self.client.get("/")
        print response.content
        self.assertContains(response, """<meta name="keywords" content="testa,testb">""")
