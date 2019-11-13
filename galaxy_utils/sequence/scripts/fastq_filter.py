# Dan Blankenberg

from __future__ import print_function

import os
import shutil
import sys

import six

from galaxy_utils.sequence.fastq import fastqReader, fastqWriter

if six.PY3:

    def execfile(path, vars):
        with open(path) as f:
            code = compile(f.read(), path, 'exec')
            exec(code, vars)


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

    i = None
    reads_kept = 0
    execfile(script_filename, globals())

    # Dan, Others: Can we simply drop the "format=input_type" here since it is specified in reader.
    # This optimization would cut runtime roughly in half (for my test case anyway). -John
    writer = fastqWriter(path=output_filename, format=input_type)
    reader = fastqReader(path=input_filename, format=input_type)
    with writer, reader:
        for i, fastq_read in enumerate(reader):
            ret_val = fastq_read_pass_filter(fastq_read)  # fastq_read_pass_filter defined in script_filename  # NOQA
            if ret_val:
                writer.write(fastq_read)
                reads_kept += 1

    if i is None:
        print("Your file contains no valid fastq reads.")
    else:
        print('Kept %s of %s reads (%.2f%%).' % (reads_kept, i + 1, float(reads_kept) / float(i + 1) * 100.0))


if __name__ == "__main__":
    main()
