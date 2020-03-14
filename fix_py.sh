#!/bin/sh

PYTHONPATH=
LINE_LENGTH=80
PY_VER=py36

if [ "$#" -ne 1 ]; then
	find . -name "*.py" | xargs -n1 -P8 ${0}
	exit 0
fi

pyupgrade --${PY_VER}-plus --exit-zero-even-if-changed "$1"
reorder-python-imports --py3-plus --exit-zero-even-if-changed "$1"
black --target-version ${PY_VER} --line-length=${LINE_LENGTH} "$1"
