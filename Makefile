CWD = $(realpath $(dir $(firstword $(MAKEFILE_LIST))))

PROJ ?= $(notdir ${CWD})
VENV ?= ${CWD}
HOST ?= $(shell hostname).local
PIP?=${VENV}/bin/pip
PYTHON?=${VENV}/bin/python

# Base python modules to install before everything else
# Some projects need wheel, numpy and cython
# before they will install correctly.
BASE?=setuptools wheel numpy cython

.DEFAULT: venv
venv: ${PYTHON}
${PYTHON}: requirements.txt
	python3 -mvenv ${VENV}
	${PIP} install --upgrade pip
	${PIP} install --upgrade ${BASE}
	${PIP} install --upgrade --requirement requirements.txt

.PHONY: clean
clean:
	@git clean -xfd

requirements.txt:
	@echo requirements.txt is missing.

.PHONY:nb
nb: ${PYTHON}
	screen -S ${PROJ} -d -m bin/jupyter-notebook --ip=${HOST}

.PHONY: debug
debug:
	$(info $${HOST}=${HOST})
	$(info $${PROJ}=${PROJ})
