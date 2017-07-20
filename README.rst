cookiecutter-pypi
----------------------------
How I package up my python projects for distribution on pypi.


Requirements:
--------------

- `cookiecutter <https://github.com/audreyr/cookiecutter>`_


Installation
-------------

1. clone the repository

2. edit cookicutter.json with your details

Usage:
---------

1. cd into the location you want use

.. code-block:: bash

    $ cd my_python_dev_folder

2. from the command line run

.. code-block:: bash

    $ cookiecutter <path-to-cloned-repository>

3. push to github

4. go to https://rawgit.com/ and generate a production url for logo_full.svg. Insert it into README.rst and index.rst.