#!/bin/sh

isort --apply --settings-path ../setup.cfg *.py
black --py36 --line-length 79 *.py

git add *.py
git commit -m "isorted and blackened python files"
