from django.contrib import admin
from django.conf import settings
from django.contrib.contenttypes.admin import GenericTabularInline

from metatags.models import URLMetatag, ContentMetatag


class MetatagInline(GenericTabularInline):
    model = ContentMetatag
    extra = 0


admin.site.register(URLMetatag, admin.ModelAdmin)

# Hook the metatag inlines into the admin for selected models
if hasattr(settings, "METATAGS") and "INLINE_MODELS" in settings.METATAGS:
    for model, admin_model in admin.site._registry.items():
        if "%s.%s" % (model._meta.app_label, model._meta.model_name) \
                in settings.METATAGS["INLINE_MODELS"]:
            admin_model.inlines = list(admin_model.inlines) + [MetatagInline]
