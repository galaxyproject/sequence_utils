#!/bin/bash

usage() {
cat << EOF
Usage: ${0##*/} [-i] /path/to/tools-devteam...
Sync sequence_util test scripts and data with tools-devteam content (or vice versa if -i).

EOF
}

if [ $# -lt 1 ]; then
    usage
    exit 1
fi

invert=0
OPTIND=1
while getopts ":i" opt; do
    case "$opt" in
        h)
            usage
            exit 0
            ;;
        i)
            invert=1
            ;;
        '?')
            usage >&2
            exit 1
            ;;
    esac
done
shift "$((OPTIND-1))" # Shift off the options and optional --.

PROJECT_DIRECTORY="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_TEST_DIR=$PROJECT_DIRECTORY/tests
TOOLS_DEVTEAM=$1

TEST_FILES=(
    tool_collections/galaxy_sequence_utils/fastq_to_tabular/test-data/sanger_full_range_original_sanger.fastqsanger
    tool_collections/galaxy_sequence_utils/fastq_to_tabular/test-data/fastq_to_tabular_out_1.tabular
    tool_collections/galaxy_sequence_utils/fastq_manipulation/test-data/fastq_trimmer_out1.fastqsanger
    tool_collections/galaxy_sequence_utils/fastq_combiner/test-data/fastq_combiner_in_1.fasta
    tool_collections/galaxy_sequence_utils/fastq_combiner/test-data/fastq_combiner_no_qual_decimal_out_1.fastqsanger
)


if [ "$invert" -ne "1" ];
then

    for f in "${TEST_FILES[@]}"
    do
        filename=`basename $f`
        cp $PROJECT_DIRECTORY/tests/$filename $TOOLS_DEVTEAM/$f
    done

else
    for f in "${TEST_FILES[@]}"
    do
        filename=`basename $f`
        cp $TOOLS_DEVTEAM/$f $PROJECT_DIRECTORY/tests/$filename 
    done

fi
