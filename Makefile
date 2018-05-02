# Config

# Makefile directory
MK_DIR = $(realpath $(dir $(firstword $(MAKEFILE_LIST))))

# Project name
PROJ ?= $(notdir ${MK_DIR})
# Virtual environment path
VENV ?= ${MK_DIR}
# Hostname
HOST:=$(shell hostname).local
# Executable paths
PIP:=${VENV}/bin/pip
PYTHON:=${VENV}/bin/python

# Base python modules to install before everything else
# Some projects need wheel, numpy and cython
# before they will install correctly.
BASE_MODULES?=setuptools wheel numpy cython

# Targets
.DEFAULT: all
.PHONY: all
all:
	$(error No default target)

.PHONY: venv
venv: ${PYTHON}

${PYTHON}: requirements.txt
	${MAKE} clean
	python3 -mvenv ${VENV}
	${PIP} install --upgrade pip
	${PIP} install --upgrade ${BASE_MODULES}
	${PIP} install --upgrade --requirement ${<}

.PHONY: clean
clean:
	@git clean -xfd

requirements.txt:
	$(error r${@} is missing.)

.PHONY:nb
nb:
	screen -S ${PROJ} -d -m bin/jupyter-notebook --ip=${HOST}

.PHONY: debug
debug:
	$(info $${MK_DIR}=${MK_DIR})
	$(info $${HOST}=${HOST})
	$(info $${PROJ}=${PROJ})
