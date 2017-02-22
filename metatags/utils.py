from django.conf import settings


def get_tag_name_choices():
    tag_dict = {
        "title": "Title",
        "description": "Description",
        "keywords": "Keywords",
        "og:title": "Open Graph Title (95 chars)",
        "og:type": "Open Graph Type",
        "og:image": "Open Graph Image",
        "og:url": "Open Graph Url",
        "og:description": "Open Graph Description",
        "fb:admins": "Facebook Admins (FB ids)",
        "twitter:card": "Twitter Card Type (default is summary)",
        "twitter:url": "Twitter URL",
        "twitter:title": "Twitter Title (70 chars)",
        "twitter:description": "Twitter Description (200 chars)",
        "twitter:image": "Twitter image",
        }

    # Get extra tags from settings
    if hasattr(settings, "METATAGS") and "tag_options" in settings.METATAGS:
        tag_dict.update(settings.METATAGS["tag_options"])

    # Build the tag option tuples
    return [(name, tag_dict[name]) for name in sorted(tag_dict.keys())
            if name and tag_dict[name]]
