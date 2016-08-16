MAD Web
==============================

Main hub for MAD online

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django


.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://raw.githubusercontent.com/txcsmad/MAD-Web/master/LICENSE
    :alt: MIT Licensed


Usage
------------

Install Python 3.5, Postgres, and Sass. Use pip to install the local requirements. Create a Postgres database named `mad_web` and a user with your username. To use the bundled run configurations, install PyCharm.

Settings
------------

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
~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ py.test


Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html




Deployment
----------
How to setup and install
Requirements:
NPM, Python3
::

    $ git clone git@github.com:txcsmad/MAD-Web.git

Make sure you are using the pip for Python 3
::
    $ pip install -r /path/to/requirements.txt
    $ npm install
    
Install with DigitalOcean: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04

Note: Has to be atleast $10 droplet for initial setup for npm install as 520mb is too little to install everything.

SSL/HTTPS: https://letsencrypt.org/

Updating Process on Server
----------
1) Pull from master
2) gulp
3) python3 manager.py collectstatic
4) sudo systemctl restart gunicorn && sudo systemctl restart nginx
