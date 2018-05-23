cookiecutter-python
======================
How to setup Envirnexus Python projects


Requirements:
--------------

- `cookiecutter <https://github.com/audreyr/cookiecutter>`_


Installation
-------------

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/blueskyideas/cookiecutter-python.git

2. Edit the ``cookicutter.json`` file with your details

Typical Project Setup Steps:
------------------------------

1. Navigate to the location where the project repository will reside:

.. code-block:: bash

    $ cd my_python_dev_folder

2. From the command line, run:

.. code-block:: bash

    $ cookiecutter path/to/cloned/cookiecutter-python

3. Create a project repository in GitHub matching the name used when cookie cutting. Do not initialize with README, license, or gitignore files

4. Push the project repository to GitHub:

.. code-block:: bash

    $ git init
    $ git add --all
    $ git commit -am "initial commit"
    $ git remote add origin <repo_url>
    $ git push --set-upstream origin master


