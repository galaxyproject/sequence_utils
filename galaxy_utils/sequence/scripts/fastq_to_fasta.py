# Dan Blankenberg

from __future__ import print_function

import sys

from galaxy_utils.sequence.fasta import fastaWriter
from galaxy_utils.sequence.fastq import fastqReader


def main():
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    input_type = sys.argv[3] or 'sanger'  # input type should ordinarily be unnecessary

    num_reads = None
    fastq_read = None
    out = fastaWriter(path=output_filename, format="fasta")
    for num_reads, fastq_read in enumerate(fastqReader(path=input_filename, format=input_type)):
        out.write(fastq_read)
    out.close()
    if num_reads is None:
        print("No valid FASTQ reads could be processed.")
    else:
        print("%i FASTQ reads were converted to FASTA." % (num_reads + 1))


if __name__ == "__main__":
    main()
