#!/usr/bin/env bash
# Script to quickly sync photos from an SD card to a local directory

# Setup
HOST=`hostname`
SD_CARD=${SD_CARD:-mmcblk0p1}
SYNC_ROOT=${SYNC_ROOT:-/data/pictures}

# Sync photos on my laptop to my local pictures directory.
DIR=`date --iso-8601="date"`

# Cameras, especially "Action Cams" have a bad habit of corrupting
# a partition.
fsck  /dev/${SD_CARD}

# Create a mountpoint.
mkdir -p /mnt/sdcard

# Mount the SD card.
mount /dev/${SD_CARD} /mnt/sdcard
# Create a dest dir
mkdir -p ${SYNC_ROOT}/${DIR}
# Sync
rsync -aP /mnt/sdcard/ ${SYNC_ROOT}/${DIR}/

# Mark the SD card as synced.
umount /mnt/sdcard

echo ${SYNC_ROOT}/${DIR}

# Exit.
exit 0
