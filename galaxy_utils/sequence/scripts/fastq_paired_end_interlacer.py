# Florent Angly
from __future__ import print_function

import sys

from galaxy_utils.sequence.fastq import (
    fastqJoiner,
    fastqNamedReader,
    fastqReader,
    fastqWriter,
)


def main():
    mate1_filename = sys.argv[1]
    mate1_type = sys.argv[2] or 'sanger'
    mate2_filename = sys.argv[3]
    mate2_type = sys.argv[4] or 'sanger'
    outfile_pairs = sys.argv[5]
    outfile_singles = sys.argv[6]

    if mate1_type != mate2_type:
        print("WARNING: You are trying to interlace files of two different types: %s and %s." % (mate1_type, mate2_type))
        return

    type = mate1_type
    joiner = fastqJoiner(type)

    nof_singles = 0
    nof_pairs = 0
    i = None
    j = None

    out_pairs = fastqWriter(path=outfile_pairs, format=type)
    out_singles = fastqWriter(path=outfile_singles, format=type)
    mate2_input = fastqNamedReader(path=mate2_filename, format=type)
    mate1_input = fastqNamedReader(path=mate1_filename, format=type)
    reader1 = fastqReader(path=mate1_filename, format=type)
    reader2 = fastqReader(path=mate2_filename, format=type)

    with out_pairs, out_singles, mate2_input, mate1_input, reader1, reader2:
        # Pairs + singles present in mate1
        for i, mate1 in enumerate(reader1):
            mate2 = mate2_input.get(joiner.get_paired_identifier(mate1))
            if mate2:
                out_pairs.write(mate1)
                out_pairs.write(mate2)
                nof_pairs += 1
            else:
                out_singles.write(mate1)
                nof_singles += 1

        # Singles present in mate2
        for j, mate2 in enumerate(reader2):
            mate1 = mate1_input.get(joiner.get_paired_identifier(mate2))
            if not mate1:
                out_singles.write(mate2)
                nof_singles += 1

    if (i is None) and (j is None):
        print("Your input files contained no valid FASTQ sequences.")
    else:
        print('There were %s single reads.' % (nof_singles))
        print('Interlaced %s pairs of sequences.' % (nof_pairs))


if __name__ == "__main__":
    main()
