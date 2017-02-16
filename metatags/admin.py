from django.contrib import admin
from django.conf import settings
from django.contrib.contenttypes.admin import GenericTabularInline

from metatags.models import URLMetatag, ContentMetatag


# TODO: Be greedy
# TODO: What happens on modelbase

class MetatagInline(GenericTabularInline):
    model = ContentMetatag
    extra = 0


admin.site.register(URLMetatag, admin.ModelAdmin)

# Hook the metatag inlines into the admin for selected models
if hasattr(settings, "METATAGS") and "inline_models" in settings.METATAGS:
    for model, admin_model in admin.site._registry.items():
        if "%s.%s" % (model._meta.app_label, model._meta.model_name) \
                in settings.METATAGS["inline_models"] \
                and MetatagInline not in admin_model.inlines:
            admin_model.inlines = list(admin_model.inlines) + [MetatagInline]
