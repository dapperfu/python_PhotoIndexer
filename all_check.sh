#!/bin/sh

# Open 'bad' files with geany: 
# ./all_check.sh  | grep "^pydarknet" | cut -f1 -d":" | sort | uniq | xargs geany
find pydarknet -name "*.py" | xargs -n1 ./check.sh

