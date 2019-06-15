# Dan Blankenberg
from __future__ import print_function

import argparse
import sys

from galaxy_utils.sequence.fastq import (
    fastqAggregator,
    fastqReader,
    fastqVerboseErrorReader,
    fastqWriter,
)


class Groomer():

    def run(self, args):
        input_filename = args.input_filename
        input_type = args.input_type
        output_filename = args.output_filename
        output_type = args.output_type
        force_quality_encoding = args.force_quality_encoding
        summarize_input = args.summarize_input == 'summarize_input'
        fix_id = args.fix_id
        if force_quality_encoding == 'None':
            force_quality_encoding = None

        aggregator = fastqAggregator()
        out = fastqWriter(
            path=output_filename, format=output_type, 
            force_quality_encoding=force_quality_encoding)
        read_count = None
        if summarize_input:
            reader_type = fastqVerboseErrorReader
        else:
            reader_type = fastqReader
        reader = reader_type(
            path=input_filename, format=input_type, 
            apply_galaxy_conventions=True, fix_id=fix_id)

        for read_count, fastq_read in enumerate(reader):
            if summarize_input:
                aggregator.consume_read(fastq_read)
            out.write(fastq_read)
        out.close()
    
        self._print_output(
            read_count, input_type, output_type, summarize_input, aggregator)
    
    def _print_output(
            self, read_count, input_type, output_type, summarize_input, aggregator):
        if read_count is not None:
           print(
               "Groomed %i %s reads into %s reads." % 
               (read_count + 1, input_type, output_type))
           if input_type != output_type and 'solexa' in [input_type, output_type]:
               print("Converted between Solexa and PHRED scores.")
           if summarize_input:
               print("Based upon quality and sequence, the input data is valid for: %s" 
                     % (", ".join(aggregator.get_valid_formats()) or "None"))
               ascii_range = aggregator.get_ascii_range()
               decimal_range = aggregator.get_decimal_range()

               # print using repr, since \x00 (null) causes info truncation 
               #   in galaxy when printed
               print("Input ASCII range: %s(%i) - %s(%i)" % (
                     repr(ascii_range[0]), ord(ascii_range[0]), 
                     repr(ascii_range[1]), ord(ascii_range[1])))  
               print("Input decimal range: %i - %i" % (decimal_range[0], decimal_range[1]))
        else:
           print("No valid FASTQ reads were provided.")


def main():
    Groomer().run(_get_args())


def _get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_filename', help='file to groom')
    parser.add_argument('input_type', help='input FASTQ quality scores type')
    parser.add_argument('output_filename', help='groomed output file')
    parser.add_argument('output_type', help='input FASTQ quality scores type')
    parser.add_argument('force_quality_encoding', help='force quality score encoding')
    parser.add_argument('summarize_input', help='summarize input data')
    parser.add_argument('--fix_id', help='fix inconsistent identifiers', action='store_true')
    return parser.parse_args()


if __name__ == "__main__":
    main()

