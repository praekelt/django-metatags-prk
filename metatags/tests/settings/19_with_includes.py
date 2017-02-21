from metatags.tests.settings.base_19 import *

METATAGS = {
    "inline_models": {"tests.dummymodel1"},
    "tag_options": {
        "test_tag": "Test Tag",
        "title": "Modified Title",
    }
}

TEST_EXCLUDES = [
    "test_no_settings",
    "test_exclude_settings",
]
