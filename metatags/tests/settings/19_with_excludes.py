from metatags.tests.settings.base_19 import *

METATAGS = {
    "exclude_inline_models": {"tests.dummymodel2"},
    "tag_options": {
        "test_tag": "Test Tag",
        "title": "",
    }
}

TEST_EXCLUDES = [
    "test_no_settings",
    "test_include_settings",
]
