#!/usr/bin/env bash

NUM=$1
IMG=$2
DIR=`date --iso-8601="date"`
mkdir -p ~/Pictures/${DIR}/${NUM}
cp "$IMG" ~/Pictures/${DIR}/${NUM}
