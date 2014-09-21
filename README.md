[![Build Status](https://travis-ci.org/Wilfred/simpla-vortaro.svg?branch=master)](https://travis-ci.org/Wilfred/simpla-vortaro)
[![Coverage Status](https://img.shields.io/coveralls/Wilfred/simpla-vortaro.svg)](https://coveralls.io/r/Wilfred/simpla-vortaro?branch=master)
[![Requirements Status](https://requires.io/github/Wilfred/simpla-vortaro/requirements.png?branch=master)](https://requires.io/github/Wilfred/simpla-vortaro/requirements/?branch=master)

*La Simpla Vortaro* is a Django website intended to push what's possible
with online Esperanto dictionaries.

The main areas of interest:

* built on Django
* simple, logical interface
* spell checking and orthography flexibility (unicode, x-system, h-system)
* morphology analysis
* definitions courtesy of La Reta Vortaro

AGPLv3 licence, see COPYING for details.

Development
-----------

Create a virtual environment:

    $ mkdir -p ~/.envs
    $ virtualenv ~/.envs/simplavortaro
    $ . ~/.envs/simplavortaro/bin/activate
    $ pip install -r requirements_pinned.txt
    
Then copy word.db from the GitHub downloads page for this project. It
should be in the root of the project with the name `word_db`. Finally:

    $ python manage.py runserver

Creating a database
-------------------

You can create a database of definitions from the XML files provided
by Reta Vortaro. There's a separate GitHub project called
ReVo-utilities, which you can use to create a JSON file of
definitions.

Copy the JSON file to the root of the project and call it
`dictionary.json`. You can then create a database with:

    $ python manage.py flush`
    $ python manage.py shell`
    In [1]: %run initialise_database.py`
    
    
Running the tests
-----------------

The tests require production data, since the entire site is read only
anyway. Make sure you have `word_db`.

    $ DJANGO_SETTINGS_MODULE=settings python test_parser.py

Updating requirements
---------------------

You can find out which packages are out of date with:

    $ pip-review

We also keep a dump of a known-good set of packages, which you can
update with:

    $ pip freeze > requirements_pinned.txt

Deployment
----------

Make sure you turn off debug in settings.py.
