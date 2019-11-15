# Dan Blankenberg
from __future__ import print_function

import sys

from galaxy_utils.sequence.fastq import (
    fastqReader,
    fastqSplitter,
    fastqWriter,
)


def main():
    # Read command line arguments
    input_filename = sys.argv[1]
    input_type = sys.argv[2] or 'sanger'
    output1_filename = sys.argv[3]
    output2_filename = sys.argv[4]

    splitter = fastqSplitter()
    i = None
    skip_count = 0

    writer1 = fastqWriter(path=output1_filename, format=input_type)
    writer2 = fastqWriter(path=output2_filename, format=input_type)
    reader = fastqReader(path=input_filename, format=input_type)
    with writer1, writer2, reader:
        for i, fastq_read in enumerate(reader):
            read1, read2 = splitter.split(fastq_read)
            if read1 and read2:
                writer1.write(read1)
                writer2.write(read2)
            else:
                skip_count += 1

    if i is None:
        print("Your file contains no valid FASTQ reads.")
    else:
        print('Split %s of %s reads (%.2f%%).' % (i - skip_count + 1, i + 1, float(i - skip_count + 1) / float(i + 1) * 100.0))


if __name__ == "__main__":
    main()
