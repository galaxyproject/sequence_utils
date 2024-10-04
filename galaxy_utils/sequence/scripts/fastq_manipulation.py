# Dan Blankenberg

import importlib.util
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

    # Save script file for debugging/verification info later
    os.makedirs(additional_files_path, exist_ok=True)
    new_script_path = os.path.join(additional_files_path, 'script.py')
    shutil.copy(script_filename, new_script_path)

    spec = importlib.util.spec_from_file_location(
        "fastq_manipulator",
        new_script_path,
    )
    assert spec
    fastq_manipulator = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(fastq_manipulator)
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
        print(f'Manipulated {reads_manipulated} of {i + 1} reads ({float(reads_manipulated) / float(i + 1) * 100.0:.2f}%).')


if __name__ == "__main__":
    main()
