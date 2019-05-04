# KISS PhotoSorter

Stuff for managing the daily growing number of personal photos and videos I shoot.

The week before one huge 'embedded' project was due in college our team threw away all code and went back to zero. Implementing the "KISS Protocol". 

## Problem Statement

I bought my first digital camera in 2002. My first digital camcorder in 2003.

Then college:

Resulting in this:

	$ zfs get used keg/Pictures
	NAME          PROPERTY  VALUE  SOURCE
	keg/Pictures  used      2.44T  -

	$ zfs get used keg/Videos
	NAME        PROPERTY  VALUE  SOURCE
	keg/Videos  used      1.02T  -

Then Kids:

    $ date; zfs get used keg/Pictures
    Fri May  3 21:38:49 EDT 2019
    NAME          PROPERTY  VALUE  SOURCE
    keg/Pictures  used      3.14T  -

    $ date; zfs get used keg/Videos
    Fri May  3 21:39:11 EDT 2019
    NAME        PROPERTY  VALUE  SOURCE
    keg/Videos  used      1.31T  -

## Stack

- Jenkins (or cron).
- Bash.
- Exiftool.