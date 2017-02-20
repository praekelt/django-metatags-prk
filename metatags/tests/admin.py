from django.contrib import admin
from metatags.tests.models import DummyModel1, DummyModel2


admin.site.register(DummyModel1, admin.ModelAdmin)
admin.site.register(DummyModel2, admin.ModelAdmin)
