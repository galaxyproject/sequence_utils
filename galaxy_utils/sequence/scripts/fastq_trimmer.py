# Dan Blankenberg


import sys

from galaxy_utils.sequence.fastq import fastqReader, fastqWriter


def main():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    left_offset = sys.argv[3]
    right_offset = sys.argv[4]
    percent_offsets = sys.argv[5] == 'offsets_percent'
    input_type = sys.argv[6] or 'sanger'
    keep_zero_length = sys.argv[7] == 'keep_zero_length'

    num_reads_excluded = 0
    num_reads = None

    writer = fastqWriter(path=output_filename, format=input_type)
    reader = fastqReader(path=input_filename, format=input_type)
    with writer, reader:
        for num_reads, fastq_read in enumerate(reader):
            if percent_offsets:
                left_column_offset = int(round(float(left_offset) / 100.0 * float(len(fastq_read))))
                right_column_offset = int(round(float(right_offset) / 100.0 * float(len(fastq_read))))
            else:
                left_column_offset = int(left_offset)
                right_column_offset = int(right_offset)
            if right_column_offset != 0:
                right_column_offset = -right_column_offset
            else:
                right_column_offset = None
            fastq_read = fastq_read.slice(left_column_offset, right_column_offset)
            if keep_zero_length or len(fastq_read):
                writer.write(fastq_read)
            else:
                num_reads_excluded += 1

    if num_reads is None:
        print("No valid FASTQ reads could be processed.")
    else:
        print(f"{num_reads + 1:d} FASTQ reads were processed.")
    if num_reads_excluded:
        print(f"{num_reads_excluded:d} reads of zero length were excluded from the output.")


if __name__ == "__main__":
    main()
