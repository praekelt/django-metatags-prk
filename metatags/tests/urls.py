from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic.base import TemplateView

from metatags.tests.views import DummyModel1View


urlpatterns = [
    url(
        r"^$",
        TemplateView.as_view(template_name="tests/home.html"),
        name="home"
    ),
    url(
        r"^dummymodel1/(?P<pk>\d+)/$",
        DummyModel1View.as_view(),
        name="dummymodel1-detail"
    ),
    url(
        r"^admin/",
        include(admin.site.urls)
    ),
]


admin.autodiscover()
