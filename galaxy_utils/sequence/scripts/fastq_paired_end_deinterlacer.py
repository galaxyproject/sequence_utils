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
    input_filename = sys.argv[1]
    input_type = sys.argv[2] or 'sanger'
    mate1_filename = sys.argv[3]
    mate2_filename = sys.argv[4]
    single1_filename = sys.argv[5]
    single2_filename = sys.argv[6]

    type = input_type
    joiner = fastqJoiner(type)
    i = None
    skip_count = 0
    found = {}

    mate1_out = fastqWriter(path=mate1_filename, format=type)
    mate2_out = fastqWriter(path=mate2_filename, format=type)
    single1_out = fastqWriter(path=single1_filename, format=type)
    single2_out = fastqWriter(path=single2_filename, format=type)
    reader1 = fastqNamedReader(path=input_filename, format=type)
    reader2 = fastqReader(path=input_filename, format=type)

    with mate1_out, mate2_out, single1_out, single2_out, reader1, reader2:

        for i, read in enumerate(reader2):

            if read.identifier in found:
                del found[read.identifier]
                continue

            mate1 = reader1.get(read.identifier)

            mate2 = reader1.get(joiner.get_paired_identifier(mate1))

            if mate2:
                # This is a mate pair
                found[mate2.identifier] = None
                if joiner.is_first_mate(mate1):
                    mate1_out.write(mate1)
                    mate2_out.write(mate2)
                else:
                    mate1_out.write(mate2)
                    mate2_out.write(mate1)
            else:
                # This is a single
                skip_count += 1
                if joiner.is_first_mate(mate1):
                    single1_out.write(mate1)
                else:
                    single2_out.write(mate1)

    if i is None:
        print("Your input file contained no valid FASTQ sequences.")
    else:
        if skip_count:
            print('There were %i reads with no mate.' % skip_count)
        print('De-interlaced %s pairs of sequences.' % ((i - skip_count + 1) / 2))


if __name__ == "__main__":
    main()
