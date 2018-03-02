#!/usr/bin/env bash

# Sync photos on my laptop to my local pictures directory.

# Root folder. 
ROOT=/pictures
# Temporary local directory.
DIR=`date --iso-8601="seconds"`

fsck /dev/mmcblk0p1
mkdir -p /mnt/sdcard
mount /dev/mmcblk0p1 /mnt/sdcard
mkdir -p $ROOT/$DIR
rsync -aP /mnt/sdcard/ $ROOT/$DIR/
umount /mnt/sdcard
