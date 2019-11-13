# Dan Blankenberg

from __future__ import print_function

import imp
import os
import shutil
import sys

from galaxy_utils.sequence.fastq import fastqReader, fastqWriter


def main():
    # Read command line arguments
    input_filename = sys.argv[1]
    script_filename = sys.argv[2]
    output_filename = sys.argv[3]
    additional_files_path = sys.argv[4]
    input_type = sys.argv[5] or 'sanger'

    # Save script file for debuging/verification info later
    os.mkdir(additional_files_path)
    shutil.copy(script_filename, os.path.join(additional_files_path, 'debug.txt'))

    fastq_manipulator = imp.load_module('fastq_manipulator', open(script_filename), script_filename, ('', 'r', imp.PY_SOURCE))
    i = None
    reads_manipulated = 0

    writer = fastqWriter(path=output_filename, format=input_type)
    reader = fastqReader(path=input_filename, format=input_type)
    with writer, reader:
        for i, fastq_read in enumerate(reader):
            new_read = fastq_manipulator.match_and_manipulate_read(fastq_read)
            if new_read:
                writer.write(new_read)
            if new_read != fastq_read:
                reads_manipulated += 1

    if i is None:
        print("Your file contains no valid FASTQ reads.")
    else:
        print('Manipulated %s of %s reads (%.2f%%).' % (reads_manipulated, i + 1, float(reads_manipulated) / float(i + 1) * 100.0))


if __name__ == "__main__":
    main()
