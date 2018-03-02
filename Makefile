VENV?=.venv
PIP?=${VENV}/bin/pip
PYTHON?=${VENV}/bin/python

BASE?=setuptools wheel numpy cython

.DEFAULT: venv
venv: ${VENV}
${VENV}: requirements.txt
	python3 -mvenv ${VENV}
	${PIP} install --upgrade pip
	${PIP} install --upgrade ${BASE}
	${PIP} install -r requirements.txt

.PHONY: clean
clean:
	@git clean -xfd

requirements.txt:
	@echo requirements.txt is missing.

.PHONY: lazy
lazy:
	autopep8 --in-place --aggressive --aggressive --aggressive *.py
	isort --apply *.py
