VENV = $(realpath $(dir $(firstword $(MAKEFILE_LIST))))
PIP?=${VENV}/bin/pip
PYTHON?=${VENV}/bin/python

BASE?=setuptools wheel numpy cython

.DEFAULT: venv
venv: ${PYTHON}
${PYTHON}: requirements.txt
	python3 -mvenv ${VENV}
	${PIP} install --upgrade pip
	${PIP} install --upgrade ${BASE}
	${PIP} install -r requirements.txt

.PHONY: clean
clean:
	@git clean -xfd

requirements.txt:
	@echo requirements.txt is missing.
