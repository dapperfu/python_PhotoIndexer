#!/usr/bin/env tcsh
# Script to quickly sync photos from an SD card to a local directory

# Setup
set HOST=`hostname`
if ( ${HOST} == "m6700" ) then
   set SD_CARD=mmcblk0p1
   set SYNC_ROOT=/net/8600k.local/mnt/vault/pictures/sync
else if ( ${HOST} == "4770k" ) then
   echo Host "${HOST}" not configured.
   exit 1
else
   echo Host "${HOST}" not configured.
   exit 1
endif

# Sync photos on my laptop to my local pictures directory.
set DIR=`date --iso-8601="seconds" | sed "s/\:/_/g"`

# Cameras, especially "Action Cams" have a bad habit of corrupting
# a partition.
fsck -a /dev/${SD_CARD}

# Create a mountpoint.
mkdir -p /mnt/sdcard

# Mount the SD card.
mount /dev/${SD_CARD} /mnt/sdcard
# Create a dest dir
mkdir -p ${SYNC_ROOT}/$DIR
# Sync
rsync -aP /mnt/sdcard/ ${SYNC_ROOT}/$DIR/

# Mark the SD card as synced.
touch "/mnt/sdcard/.synced_`date +%Y%b%d_%H%M%S`"
# Unmount
umount /mnt/sdcard

# Exit.
exit 0
