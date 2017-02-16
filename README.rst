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


ObjectMetaTag

* content_object: The object that this metatag will render for. This is a generic foreign key, and will be added as an inline.

* name: A predefined set of tag names.

* content: The tag content


Usage
-----

Add the following to the base template in the head section::

    {% load metatag_tags %}

    {% if object %}
        {% metatags object %}
    {% else %}
        {% metatags %}
    {% endif %}

xxxx This will find all metatags that match the object or the url.
