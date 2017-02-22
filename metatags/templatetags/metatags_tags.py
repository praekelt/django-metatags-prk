import re

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import NoReverseMatch, resolve, reverse
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.text import mark_safe

from metatags.models import URLMetatag, ContentMetatag


register = template.Library()

# Some tags take the form <meta property= instead of <meta name=
tag_name_map = {
        "og:title": "property",
        "og:type": "property",
        "og:image": "property",
        "og:url": "property",
        "og:description": "property",
        "fb:admins": "property",
}


@register.inclusion_tag("metatags/inclusion_tags/metatags.html",
                        takes_context=True)
def metatags(context, obj=None, **kwargs):
    request = context["request"]
    # Get tags for the URL
    tags = list(URLMetatag.permitted.all())
    tags.sort(lambda a, b: cmp(len(b.url), len(a.url)))

    # Assemble map with best matches
    tag_map = {}
    request_path = request.get_full_path()
    for tag in tags:
        if tag.name in tag_map:
            continue
        if re.search(r"%s" % tag.url, request_path):
            tag_map[tag.name] = tag.content

    # Overrides for specific fields presented as keyword args
    for k, v in kwargs.items():
        if v:
            tag_map[k] = v

    # Override tags with the object tags
    if not obj and "object" in context:
        obj = context["object"]

    if obj:
        reverse_type = ContentType.objects.get_for_model(obj)
        tags = ContentMetatag.permitted.filter(
            content_type__pk=reverse_type.id,
            object_id=obj.id
        )
        for tag in tags:
            tag_map[tag.name] = tag.content

    tags = []
    for k, v in tag_map.items():
        if k in tag_name_map.keys():
            tags.append({"name": k, "content": v, "type": tag_name_map[k]})
        else:
            tags.append({"name": k, "content": v, "type": "name"})

    return {
        "tags": tags,
        "tag_name_map": tag_name_map
    }
