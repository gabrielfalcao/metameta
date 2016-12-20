TZ	:= UTC
OSNAME	:= $(shell uname | tr '[:upper:]' '[:lower:]')

ifeq ($(OSNAME), darwin)
OPEN	:= open
else
OPEN	:= gnome-open
endif


all: bootstrap tests

bootstrap: remove clean deps

tests: lint unit

deps:
	@pip install -U setuptools
	@pip install -U pip
	@pip install -r development.txt

build: clean html-docs
	@(>&2 python setup.py sdist>/dev/null)

remove:
	-@(>&2 pip uninstall -y metameta>/dev/null)

clean:
	@rm -rfv 'dist'
	@rm -rfv 'docs/build'
	@find . -name '*.pyc' -exec rm -vf {} \;

lint:
	@find metameta -name '*.py' | grep -v node | xargs flake8 --ignore=E501 --max-complexity=6

unit:
	nosetests --cover-erase --rednose --cover-erase tests/unit

functional:
	nosetests --with-spec --spec-color tests/functional

release: tests
	@./.release
	@python setup.py sdist upload  -r d4v1ncy.test
	@python setup.py sdist upload  -r d4v1ncy.real

html-docs:
	cd docs && make linkcheck dummy html

docs: html-docs
	$(OPEN) docs/build/html/index.html
