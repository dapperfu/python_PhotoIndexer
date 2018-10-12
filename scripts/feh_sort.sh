#!/usr/bin/env bash

NUM=$1
IMG=$2

mkdir -p ~/Pictures/$NUM
cp "$IMG" ~/Pictures/$NUM
