from setuptools import setup
import os
import sys
PY_VER = sys.version_info

if not PY_VER >= (3, 6):
    raise RuntimeError("{{ cookiecutter.project_slug }} doesn't support Python earlier than 3.6")

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, '{{ cookiecutter.project_slug }}', '__version__.py'), 'r') as f:
    exec(f.read(), about)

def read(fname):
    with open(os.path.join(here, fname), 'r') as f:
        return str(f.read().strip())

setup(
    name='{{ cookiecutter.project_slug }}',
    version=about['__version__'],
    packages=['{{ cookiecutter.project_slug }}'],
    description="{{ cookiecutter.project_short_description }}",
    long_description='\n\n'.join((read('README.rst'), read('CHANGELOG.rst'))),
    include_package_data=True,
    install_requires=[
        
    ],
    zip_safe=False,
    author="{{ cookiecutter.full_name }}",
    author_email="{{ cookiecutter.email }}",
    license="Proprietary",
    keywords=[],
    url="https://github.com/blueskyideas/{{ cookiecutter.project_slug }}",

)

