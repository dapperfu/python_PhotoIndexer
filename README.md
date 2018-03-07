# PhotoStuffs
Stuff for managing the daily growing number of personal photos and videos I shoot.

## Problem Statement

I bought my first digital camera in 2002. My first digital camcorder in 2003.

Resulting in this:

	$ zfs get used keg/Pictures
	NAME          PROPERTY  VALUE  SOURCE
	keg/Pictures  used      2.44T  -

	$ zfs get used keg/Videos
	NAME        PROPERTY  VALUE  SOURCE
	keg/Videos  used      1.02T  -

## Stack

[PonyORM](https://ponyorm.com/):

- An exceptionally convenient syntax for writing queries
    - Automatic query optimization
    - An elegant solution for the N+1 problem
    - The online database schema editor
    - Supported databases
        - SQLite
        - PostgreSQL
        - MySQL
        - Oracle [A necessary evil for business]