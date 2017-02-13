# Dan Blankenberg

from __future__ import print_function

import sys

from galaxy_utils.sequence.fastq import fastqReader


def main():
    if len(sys.argv) != 5:
        _stop_err("Wrong number of arguments. Expect: fasta tabular desrc_split [type]")
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    descr_split = int(sys.argv[3]) - 1
    if descr_split < 0:
        _stop_err("Bad description split value (should be 1 or more)")
    input_type = sys.argv[4] or 'sanger'  # input type should ordinarily be unnecessary

    num_reads = None
    fastq_read = None
    out = open(output_filename, 'wt')
    if descr_split == 0:
        # Don't divide the description into multiple columns
        for num_reads, fastq_read in enumerate(fastqReader(path=input_filename, format=input_type)):
            out.write("%s\t%s\t%s\n" % (fastq_read.identifier[1:].replace('\t', ' '), fastq_read.sequence.replace('\t', ' '), fastq_read.quality.replace('\t', ' ')))
    else:
        for num_reads, fastq_read in enumerate(fastqReader(path=input_filename, format=input_type)):
            words = fastq_read.identifier[1:].replace('\t', ' ').split(None, descr_split)
            # pad with empty columns if required
            words += [""] * (descr_split - len(words))
            out.write("%s\t%s\t%s\n" % ("\t".join(words), fastq_read.sequence.replace('\t', ' '), fastq_read.quality.replace('\t', ' ')))
    out.close()
    if num_reads is None:
        print("No valid FASTQ reads could be processed.")
    else:
        print("%i FASTQ reads were converted to Tabular." % (num_reads + 1))


def _stop_err(msg):
    sys.stderr.write(msg)
    sys.exit()


if __name__ == "__main__":
    main()
