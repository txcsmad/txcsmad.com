MAD Web
=======

Main hub for MAD online

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/txcsmad/MAD-Web/master/LICENSE
    :alt: MIT Licensed


Usage
-----

Install Python 3.5, Postgres, and Sass. Use pip to install the local requirements. Create a Postgres database named `mad_web` and a user with your username. To use the bundled run configurations, install PyCharm.

Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run manage.py test
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test


Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Local Deployment
----------

First time
^^^^^^^^^^
Install Postgres app(http://postgresapp.com/) and make it run
::

    $ brew install python3
    $ brew install npm
    $ git clone git@github.com:txcsmad/MAD-Web.git
    $ pip3 install -r requirements/local.txt
    $ npm install
    $ npm install --global gulp-cli
    $ createdb mad_web
    $ python3 manage.py migrate
    $ python4 manage.py runserver --settings=config.settings.local
    
Set user to superuser & staff
^^^^^^^^^^
So you can access the /admin portal. ::
    $ psql mad_web
    mad_web# UPDATE users_user SET is_superuser = true AND is_staff = true WHERE id = 1;

Server Deployment
----------
First time
^^^^^^^^^^
Install Python3, postgres. ::

    $ git clone git@github.com:txcsmad/MAD-Web.git
    $ pip3 install -r requirements/production.txt
    $ npm install
    $ npm install --global gulp-cli
    $ createdb mad_web
    $ python3 manage.py migrate

Install a `Django stack`_ on a DigitalOcean Droplet. You will need more than the base droplet as 512Mb of RAM is too little to install everything.

.. _Django stack: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

Get SSL certificates from `Let's Encrypt`_

.. _Let's Encrypt: https://letsencrypt.org/

Rename ``config.template.json`` to ``config.json`` in ``config/settings``. The Django key should be a unique 50 character key. The site will still function for basic local testing without modifying the remaining placeholders

Updates
^^^^^^^
The MAD server is configured with an ``updatemad`` command, which is an alias for all of the below.::

    # Pull from master
    git pull origin master
    
    # migrate database changes
    python3 manage.py migrate

    # Update sass and js files
    gulp

    # Gather all static files and update them
    python3 manage.py collectstatic --noinput

    # Restart server with new code::
    sudo systemctl restart gunicorn && sudo systemctl restart nginx
