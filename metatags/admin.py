from django.contrib import admin
from django.conf import settings
from django.contrib.contenttypes.admin import GenericTabularInline

from metatags.models import URLMetatag, ContentMetatag


class MetatagInline(GenericTabularInline):
    model = ContentMetatag
    extra = 0


admin.site.register(URLMetatag, admin.ModelAdmin)


# Hook the metatag inlines into the admin for selected models
included_models = []
excluded_models = ["metatags.urlmetatag"]
if hasattr(settings, "METATAGS"):
    if "inline_models" in settings.METATAGS:
        included_models = settings.METATAGS["inline_models"]

    if "exclude_inline_models" in settings.METATAGS:
        excluded_models = list(settings.METATAGS["exclude_inline_models"]) \
            + excluded_models

for model, admin_model in admin.site._registry.items():
    model_type = "%s.%s" % (model._meta.app_label, model._meta.model_name)

    if included_models and model_type not in included_models:
        continue

    if model_type in excluded_models:
        continue

    if MetatagInline not in admin_model.inlines:
        admin_model.inlines = list(admin_model.inlines) + [MetatagInline]
