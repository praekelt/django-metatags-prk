Django Metatags
=============
**Add metatags to objects and urls**

.. image:: https://travis-ci.org/praekelt/django-metatags-prk.svg?branch=develop
    :target: https://travis-ci.org/praekelt/django-metatags-prk

.. image:: https://coveralls.io/repos/github/praekelt/django-metatags-prk/badge.svg?branch=develop
    :target: https://coveralls.io/github/praekelt/django-metatags-prk?branch=develop

.. contents:: Contents
    :depth: 5

Quick start
-----------

``django-metatags-prk`` is intended to be a standalone library, not a project, but it can be run with::

    - virtualenv ve
    - ./ve/bin/pip install -r metatags/tests/requirements/19.txt
    - ./ve/bin/python manage.py migrate --run-syncdb --settings=metatags.tests.settings.19
    - ./ve/bin/python manage.py runserver 0.0.0.0:8000 --settings=metatags.tests.settings.19


Installation
------------

#. Install the contents of ``metatags/tests/requirements/19.txt`` to your Python environment.

#. Add ``metatags`` to the ``INSTALLED_APPS`` setting, at the end of the list.


Content types
-------------

URLMetaTag:

* url: The URL or URL pattern where the tag should appear. This may be a regular expression.

* name: A predefined set of tag names.

* content: The tag content


ObjectMetaTag (Not directly visible in admin)

* content_object: The object that this metatag will render for. This is a generic foreign key, and will be added as an inline.

* name: A predefined set of tag names.

* content: The tag content


Usage
-----

To get the URLMetatags to render, add the following to the base template in the head section::

    {% load metatags_tags %}

    <head>
        {% metatags %}
    </head>

This will look for ContentMetatags on the `object` parameter on the context, with fallbacks to the best matching URLMetatags. This should be suitable for most templates that use generic content views.

If the object that the ContentMetatags are added to is not the context["object"], you can specify a specific object to get the metatags from. Assuming that the object that you added metatags to is available as `thing`::

    {% load metatags_tags %}

    <head>
        {% if thing %}
            {% metatags thing %}
        {% else %}
            {% metatags %}
        {% endif %}
    </head>

You can also provide metatags directly from the object. For example, if your object already has a title property that you want to use as default::

    {% load metatags_tags %}

    <head>
        {% if thing and thing.title %}
            {% metatags thing title=thing.title %}
        {% elif thing %}
            {% metatags thing %}
        {% else %}
            {% metatags %}
        {% endif %}
    </head>

The resolution of the tag will work as follows, taking the title tag from above as an example:

* The default title metatag is taken from the URLMetatags (on the specific URL or a matching URLpattern)

* The object title will override that, if specified as a keyword argument.

* If the object has an inline title metatag, that will override even the objects own provided title.

Advanced configuration
----------------------

By default, the ContentMetatag inlines will be added to all models in the admin. You probably do not want that. There are 2 ways to configure which models will get the inlines:

1. Only include the models you want to have inline ContentMetatags in settings.py. For example, to only have ContentMetatags on the `thing` model in the `things` app::

    METATAGS = {
        "inline_models": ["things.thing"]
    }

2. Exclude specific models in settings.py. For example, to have inlines on all admin models except the `thing` model::

    METATAGS = {
        "exclude_inline_models": ["things.thing"]
    }

Adjusting Metatag types
-----------------------

The product comes with a reasonable set of tag types. You can add more, change the option description or remove tag types from your project by adding them in settings.py. For example, you could have the following in settings.py::

    METATAGS = {
        "tag_options": {
            "test_tag": "Test Tag",
            "title": "Title tag (KEEP THIS SHORT)",
            "keywords": "",
        }
    }

This will:

* Add a `test_tag` metatag

* Change the `title` tag description in the dropdown

* Remove the `keywords` tag type
