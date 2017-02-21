from django.conf import settings


def get_tag_name_choices():
    tag_dict = {
        "title": "Title",
        "description": "Description",
        "keywords": "Keywords",
        }

    # Get extra tags from settings
    if hasattr(settings, "METATAGS") and "tag_options" in settings.METATAGS:
        tag_dict.update(settings.METATAGS["tag_options"])

    # Build the tag option tuples
    return [(name, tag_dict[name]) for name in sorted(tag_dict.keys()) \
            if name and tag_dict[name]]
