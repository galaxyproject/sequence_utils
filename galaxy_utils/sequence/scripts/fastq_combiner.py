# Dan Blankenberg

from __future__ import print_function

import sys

from galaxy_utils.sequence.fasta import (
    fastaNamedReader,
    fastaReader,
)
from galaxy_utils.sequence.fastq import (
    fastqCombiner,
    fastqFakeFastaScoreReader,
    fastqWriter,
)


def main():
    # Read command line arguments
    fasta_filename = sys.argv[1]
    fasta_type = sys.argv[2] or 'fasta'  # should always be fasta or csfasta? what if txt?
    qual_filename = sys.argv[3]
    qual_type = sys.argv[4] or 'qualsanger'  # qual454 qualsolid
    output_filename = sys.argv[5]
    force_quality_encoding = sys.argv[6]
    if force_quality_encoding == 'None':
        force_quality_encoding = None

    format = 'sanger'
    if fasta_type == 'csfasta' or qual_type == 'qualsolid':
        format = 'cssanger'
    elif qual_type == 'qualsolexa':
        format = 'solexa'
    elif qual_type == 'qualillumina':
        format = 'illumina'

    if qual_filename == 'None':
        qual_input = fastqFakeFastaScoreReader(format, quality_encoding=force_quality_encoding)
    else:
        qual_input = fastaNamedReader(open(qual_filename, 'rt'))

    fastq_combiner = fastqCombiner(format)
    i = None
    skip_count = 0

    writer = fastqWriter(path=output_filename, format=format, force_quality_encoding=force_quality_encoding)
    with writer:
        for i, sequence in enumerate(fastaReader(open(fasta_filename, 'rt'))):
            quality = qual_input.get(sequence)
            if quality:
                fastq_read = fastq_combiner.combine(sequence, quality)
                writer.write(fastq_read)
            else:
                skip_count += 1

    if i is None:
        print("Your file contains no valid FASTA sequences.")
    else:
        print(qual_input.has_data())
        print('Combined %s of %s sequences with quality scores (%.2f%%).' % (i - skip_count + 1, i + 1, float(i - skip_count + 1) / float(i + 1) * 100.0))


if __name__ == "__main__":
    main()
