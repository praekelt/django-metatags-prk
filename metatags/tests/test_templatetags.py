from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase

from metatags.models import URLMetatag, ContentMetatag
from metatags.tests.models import DummyModel1

HOME_REGEX = "^" + reverse("home") + "$"


class TemplateTagsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(TemplateTagsTestCase, cls).setUpTestData()
        cls.tag = URLMetatag.objects.create(
            name="keywords",
            content="testa,testb", url="^/$")
        cls.tag.sites = Site.objects.all()
        cls.tag.save()

        cls.model1 = DummyModel1.objects.create(title="Dummy Title 1")
        cls.model1.sites = Site.objects.all()
        cls.model1.save()


    def test_default_tags(self):
        response = self.client.get("/")
        self.assertContains(
            response,
            """<meta name="keywords" content="testa,testb">""")

    def test_model_properties(self):
        response = self.client.get("/dummymodel1/1/")
        self.assertContains(
            response,
            """<title>Dummy Title 1</title>""")

    def test_content_tags(self):
        content_tag = ContentMetatag.objects.create(
            name="title",
            content="Content Meta Title",
            content_type=ContentType.objects.get_for_model(DummyModel1),
            object_id=self.model1.pk)
        content_tag.sites = Site.objects.all()
        content_tag.save()
        response = self.client.get("/dummymodel1/1/")
        self.assertContains(
            response,
            """<title>Content Meta Title</title>""")
