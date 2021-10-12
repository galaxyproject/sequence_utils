# Dan Blankenberg


import sys

from galaxy_utils.sequence.fastq import (
    fastqAggregator,
    fastqReader,
)

VALID_NUCLEOTIDES = ['A', 'C', 'G', 'T', 'N']
VALID_COLOR_SPACE = list(map(str, range(7))) + ['.']
SUMMARY_STAT_ORDER = ['read_count', 'min_score', 'max_score', 'sum_score', 'mean_score', 'q1', 'med_score', 'q3', 'iqr', 'left_whisker', 'right_whisker']


def main():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    input_type = sys.argv[3] or 'sanger'

    aggregator = fastqAggregator()
    num_reads = None
    fastq_read = None
    with fastqReader(path=input_filename, format=input_type) as reader:
        for num_reads, fastq_read in enumerate(reader):
            aggregator.consume_read(fastq_read)
    out = open(output_filename, 'w')
    valid_nucleotides = VALID_NUCLEOTIDES
    if fastq_read:
        if fastq_read.sequence_space == 'base':
            out.write('#column\tcount\tmin\tmax\tsum\tmean\tQ1\tmed\tQ3\tIQR\tlW\trW\toutliers\tA_Count\tC_Count\tG_Count\tT_Count\tN_Count\tother_bases\tother_base_count\n')
        else:
            out.write('#column\tcount\tmin\tmax\tsum\tmean\tQ1\tmed\tQ3\tIQR\tlW\trW\toutliers\t0_Count\t1_Count\t2_Count\t3_Count\t4_Count\t5_Count\t6_Count\t._Count\tother_bases\tother_base_count\n')
            valid_nucleotides = VALID_COLOR_SPACE
    for i in range(aggregator.get_max_read_length()):
        column_stats = aggregator.get_summary_statistics_for_column(i)
        out.write(f'{i + 1:d}\t')
        out.write("{:d}\t{:d}\t{:d}\t{:d}\t{:f}\t{:f}\t{:f}\t{:f}\t{:f}\t{:d}\t{:d}\t".format(*(column_stats[key] for key in SUMMARY_STAT_ORDER)))  # noqa: SFS201
        out.write(f"{','.join(map(str, column_stats['outliers']))}\t")
        base_counts = aggregator.get_base_counts_for_column(i)
        for nuc in valid_nucleotides:
            out.write(f"{base_counts.get(nuc, 0)}\t")
        extra_nucs = sorted(nuc for nuc in base_counts.keys() if nuc not in valid_nucleotides)
        out.write(f"{','.join(extra_nucs)}\t{','.join(str(base_counts[nuc]) for nuc in extra_nucs)}\n")
    out.close()
    if num_reads is None:
        print("No valid FASTQ reads could be processed.")
    else:
        print(f"{num_reads + 1:d} FASTQ reads were processed.")
        print(
            "Based upon quality values and sequence characters, the input data is valid for:",
            ", ".join(aggregator.get_valid_formats()) or "None"
        )
        ascii_range = aggregator.get_ascii_range()
        decimal_range = aggregator.get_decimal_range()
        print(f"Input ASCII range: {repr(ascii_range[0])}({ord(ascii_range[0]):d}) - {repr(ascii_range[1])}({ord(ascii_range[1]):d})")  # print(using repr, since \x00 (null) causes info truncation in galaxy when printed)
        print(f"Input decimal range: {decimal_range[0]:d} - {decimal_range[1]:d}")


if __name__ == "__main__":
    main()
