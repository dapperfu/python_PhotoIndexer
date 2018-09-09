#!/bin/sh

echo \#\#\#\#\#\#\#\#\#\#
echo \# flake8 \#
echo \#\#\#\#\#\#\#\#\#\#
flake8 --statistics --max-line-length=79 "$1"
echo \#\#\#\#\#\#\#\#\#\#\#\#\#\#\#
echo \# pycodestyle \#
echo \#\#\#\#\#\#\#\#\#\#\#\#\#\#\#
pycodestyle --statistics --max-line-length=79 "$1"
echo \#\#\#\#\#\#\#\#\#\#\#\#\#\#
echo \# pydocstyle \#
echo \#\#\#\#\#\#\#\#\#\#\#\#\#\#
pydocstyle  --convention=numpy --verbose "$1"
