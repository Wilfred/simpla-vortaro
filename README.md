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

    $ mkvirtualenv simpla -p `which python2`
    $ pip install -r requirements_pinned.txt

I also recommend the following developer tools:

    $ pip install ipdb ipython
    
Then copy word.db from the
[GitHub downloads page for this project](https://github.com/Wilfred/simpla-vortaro/downloads). It
should be in the root of the project with the name `word_db`. Finally:

    $ python manage.py runserver

Creating a database
-------------------

You can create a database of definitions from the XML files provided
by Reta Vortaro. Use
[ReVo-utilities](https://github.com/Wilfred/ReVo-utilities) to create
a JSON file of definitions.

Copy the JSON file to the root of the project and call it
`dictionary.json`. You can then create a database with:

    $ python manage.py flush
    $ python manage.py shell
    In [1]: %run initialise_database.py
    
    
Running the tests
-----------------

The unit tests (as run by Travis) have no dependencies, and can be run
with:

    $ python manage.py test

The word parsing tests require the full dictionary dataset. Make sure
you have `word_db` set up.

    $ DJANGO_SETTINGS_MODULE=settings python _test_parser.py

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

Docker
------

Assuming you have dictionary.json locally:

```
$ docker build . -t sv
$ docker run --name sv -p 9001:9001 -t -d wilfred/simplavortaro
```

This image is [available on Docker
Hub](https://cloud.docker.com/u/wilfred/repository/docker/wilfred/simplavortaro).
