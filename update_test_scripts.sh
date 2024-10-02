#!/bin/bash

usage() {
cat << EOF
Usage: ${0##*/} [-i] /path/to/tools-devteam /path/to/tools-iuc
Sync sequence_util test data with tool repos (or vice versa if -i).

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
TOOLS_IUC=$2

TEST_FILES=(
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_to_tabular/test-data/sanger_full_range_original_sanger.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_to_tabular/test-data/fastq_to_tabular_out_1.tabular"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_manipulation/test-data/fastq_trimmer_out1.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_combiner/test-data/fastq_combiner_in_1.fasta"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_combiner/test-data/fastq_combiner_no_qual_decimal_out_1.fastqsanger"
    "$TOOLS_DEVTEAM/tools/fastq_trimmer_by_quality/test-data/sanger_full_range_quality_trimmed_out_1.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_masker_by_quality/test-data/sanger_full_range_masked_N.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_joiner/test-data/split_pair_reads_1.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_joiner/test-data/split_pair_reads_2.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_joiner/test-data/3.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_deinterlacer/test-data/paired_end_merged_errors.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_deinterlacer/test-data/paired_end_1_cleaned.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_deinterlacer/test-data/paired_end_2_cleaned.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_deinterlacer/test-data/paired_end_1_cleaned_singles.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_deinterlacer/test-data/paired_end_2_cleaned_singles.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_interlacer/test-data/paired_end_1_errors.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_interlacer/test-data/paired_end_2_errors.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_interlacer/test-data/paired_end_merged_cleaned.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_paired_end_interlacer/test-data/paired_end_merged_cleaned_singles.fastqsanger"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_stats/test-data/fastq_stats1.fastq"
    "$TOOLS_IUC/tool_collections/galaxy_sequence_utils/fastq_stats/test-data/fastq_stats_1_out.tabular"
)


if [ "$invert" -ne "1" ]; then
    for f in "${TEST_FILES[@]}"; do
        filename=$(basename "$f")
        cp "$PROJECT_DIRECTORY/tests/$filename" "$f"
    done
else
    for f in "${TEST_FILES[@]}"; do
        filename=$(basename "$f")
        cp "$f" "$PROJECT_DIRECTORY/tests/$filename"
    done
fi
