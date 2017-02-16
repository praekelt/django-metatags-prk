from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import get_script_prefix
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from metatags.managers import PermittedManager
from metatags.utils import get_tag_name_choices


class Metatag(models.Model):
    name = models.CharField(
        max_length=100,
        choices=get_tag_name_choices(),
        help_text="The name of the metatag."
    )
    content = models.CharField(
        max_length=250,
        help_text="The content of the metatag.",
    )
    sites = models.ManyToManyField(
        "sites.Site",
        help_text="Sites that this tag will appear on.",
        blank=True,
    )

    objects = models.Manager()
    permitted = PermittedManager()

    class Meta:
        abstract = True


class URLMetatag(Metatag):
    url = models.CharField(
        _("URL"),
        max_length=100,
        default="^/$",
        db_index=True,
        help_text=_("""Where on the site this metatag will appear. This value
may be a regular expression and may be very complex. A simple example
is ^/about-us/, which means any URL starting with /about-us/ will have
this metatag."""),
    )

    def __unicode__(self):
        # Use same pattern as flatpages
        return "%s -- %s" % (self.url, self.name)


class ContentMetatag(Metatag):
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(
    )
    content_object = GenericForeignKey(
        "content_type",
        "object_id",
    )
