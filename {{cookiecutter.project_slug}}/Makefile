.PHONY: docs
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
	# python run_tests.py --unit --output text --dist arch

virtualenv:
	rm -rf env
	virtualenv --python=python3.6 env
	#need to reference the virtualenv's pip
	#using . /env/bin/activate doesnt work from within a Makefile
	#"The basic issue is that a child process can not alter the parent's environment"
	./env/bin/pip install -r requirements_dev.txt