#!/usr/bin/env bash
function sortify {
echo "~~~~~ sortify ~~~~~"
if [ ${?} -eq 0 ];then
exiftool -dateFormat %Y/%m-%b/%Y%m%d_%H%M%S%%-c.%%e "-filename<FileModifyDate" "${1}"
fi
}
ARGC=$#
# This function has too few args.
if [ ${ARGC} -eq 0 ]; then
echo "${0} <input_movie>"
exit 0
fi
# This call has too many args.
if [ ${ARGC} -gt 1 ]; then
EXEC=`realpath ${0}`
for movie in "$@"
do
${EXEC} "${movie}"
done
fi
# This call is just right.
if [ ${ARGC} -eq 1 ]; then
INPUT=`realpath ${1}`
sortify "${INPUT}"
exit 0
fi
exit 99
