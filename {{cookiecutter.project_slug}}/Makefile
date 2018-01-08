.PHONY: flake8 package docs tests virtualenv_dev virtualenv_prod private_assets
flake8:
	flake8 --ignore=E501,F401,E128,E402,E731,F821 {{ cookiecutter.project_slug }}

package:
	rm -rf build dist .egg {{ cookiecutter.project_slug }}.egg-info
	python3.6 setup.py release sdist bdist_wheel

docs:
	cd docs && make html
	@echo -e "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

tests:
	./env/bin/pytest --cov={{ cookiecutter.project_slug }} --junitxml=test-reports/{{ cookiecutter.project_slug }}.xml test/
	./env/bin/coverage html

virtualenv_dev:
	rm -rf env
	virtualenv --python=python3.6 env
	./env/bin/pip install -r requirements/dev.txt
	./env/bin/pip install .
	#freeze all requirements except dev ones. This is the state of the packages during
	#testing.
	./env/bin/pip freeze > requirements/frozen_dev.txt
	#now can install extra dev packages
	./env/bin/pip install -e .[dev]

private_assets:
	rm -rf asset_env private_assets
	virtualenv --python=python3.6 asset_env
	./asset_env/bin/pip install requests
	mkdir -p private_assets
	./asset_env/bin/python ./scripts/download_assets.py


virtualenv_prod:
	rm -rf env
	virtualenv --python=python3.6 env
	#Will fail if i missed any packages in main.txt because of --require-hashes.
	./env/bin/pip install --require-hashes -r requirements/main.txt
	#doing a quick check to make sure importing works
	#have to change dir so it doesnt import the local copy
	export VIRTUALENV_DIR=$$(pwd) && cd / && \
	$$VIRTUALENV_DIR/env/bin/python -c "import {{ cookiecutter.project_slug }}; print('importing of {{ cookiecutter.project_slug }} success')"