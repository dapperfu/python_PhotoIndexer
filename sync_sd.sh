#!/usr/bin/env bash

# Sync photos on my laptop to my local pictures directory.

# Root folder. 
ROOT=/pictures
# Temporary local directory.
DIR=`date --iso-8601="seconds"`

# Cameras (especially "Action Cams" have a bad habit of corrupting 
# a partition)
fsck /dev/mmcblk0p1

# Create a mountpoint.
mkdir -p /mnt/sdcard

# Mount the SD card.
mount /dev/mmcblk0p1 /mnt/sdcard
# Create a dest dir
mkdir -p $ROOT/$DIR
# Sync
rsync -aP /mnt/sdcard/ $ROOT/$DIR/

touch "/mnt/sdcard/.synced_`date +%Y%b%d_%H%M%S`"
# Unmo
umount /mnt/sdcard
