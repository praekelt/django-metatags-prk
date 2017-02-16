from django.conf import settings

def get_tag_name_choices():
    tag_dict = {
        "title": "Title",
        "description": "Description",
        "keywords": "Keywords",
        }

    # Get extra tags from settings
    if hasattr(settings, "METATAGS") and "TAG_OPTIONS" in settings.METATAGS:
        tag_dict.update(settings.METATAGS["TAG_OPTIONS"])

    # Build the tag option tuples
    return [(name, tag_dict[name]) for name in sorted(tag_dict.keys())]
