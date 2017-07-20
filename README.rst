cookiecutter-pypi
----------------------------
How I setup my projects for distribution on pypi.


Requirements:
--------------

- `cookiecutter <https://github.com/audreyr/cookiecutter>`_


Installation
-------------

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/jeremyarr/cookiecutter-pypi.git

2. Edit the ``cookicutter.json`` file with your details

Usage:
---------

1. Navigate to the location you want use:

.. code-block:: bash

    $ cd my_python_dev_folder

2. From the command line, run:

.. code-block:: bash

    $ cookiecutter path/to/cloned/cookiecutter-pypi/repository

3. Create a repository in GitHub. Do not initialize the new repository with README, license, or gitignore files

4. Push your repository to GitHub:

.. code-block:: bash

    $ git init
    $ git commit -am "initial commit"
    $ git remote add origin <repo_url>
    $ git push --set-upstream origin master

4. Go to https://rawgit.com/ and generate a production url for ``docs/_static/logo_full.svg``. Insert it into ``README.rst`` and ``docs/index.rst`` in place of ``docs/_static/logo_full.svg``.

5. Setup jenkins build job <repo_name>1

6. Setup master as a protected branch in GitHub with status checks

7. Do a pull request to verify Jenkins is performing builds