# Config
VENV=_${PROJ}

# Environments to setup for this project
# Available options: python arduino
ENVS:=python dev

.PHONY: env.dev
env.dev: env.python
	${PYTHON} setup.py build
	${PYTHON} setup.py develop

## make_sandwich includes
# https://github.com/jed-frey/make_sandwich
include .mk_inc/env.mk
