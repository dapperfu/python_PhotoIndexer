#!/bin/sh
# Fix all files in a given directory (and below)

# Find all ".py" files in the pydarknet folder.
# For each of those files:
#    -n1: Pass them individually to fix.sh
#    -P8: Run 8 in parallel
find pydarknet -name "*.py" | xargs -n1 -P8 ./fix.sh
exit 0
