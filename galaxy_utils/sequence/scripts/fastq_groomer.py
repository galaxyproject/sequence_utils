# Dan Blankenberg
from __future__ import print_function

import argparse

from galaxy_utils.sequence.fastq import (
    fastqAggregator,
    fastqReader,
    fastqVerboseErrorReader,
    fastqWriter,
)


class Groomer():

    def __init__(self, file_handle=None):
        self.file_handle = file_handle
        args = self._get_args()
        self.input_filename = args.input_filename
        self.input_type = args.input_type
        self.output_filename = args.output_filename
        self.output_type = args.output_type
        self.force_quality_encoding = args.force_quality_encoding
        self.summarize_input = args.summarize_input == 'summarize_input'
        self.fix_id = args.fix_id

        if self.force_quality_encoding == 'None':
            self.force_quality_encoding = None

    def run(self):
        aggregator = fastqAggregator()
        out = fastqWriter(
            path=self.output_filename, format=self.output_type,
            force_quality_encoding=self.force_quality_encoding)
        if self.summarize_input:
            reader_type = fastqVerboseErrorReader
        else:
            reader_type = fastqReader
        reader = reader_type(
            fh=self.file_handle, path=self.input_filename, format=self.input_type,
            apply_galaxy_conventions=True, fix_id=self.fix_id)
        read_count = None

        for read_count, fastq_read in enumerate(reader):
            if self.summarize_input:
                aggregator.consume_read(fastq_read)
            out.write(fastq_read)
        out.close()

        self._print_output(read_count, aggregator)

    def _print_output(self, read_count, aggregator):
        if read_count is not None:
            print("Groomed %i %s reads into %s reads." % (read_count + 1, self.input_type, self.output_type))
            if self.input_type != self.output_type and 'solexa' in [self.input_type, self.output_type]:
                print("Converted between Solexa and PHRED scores.")
            if self.summarize_input:
                print(
                    "Based upon quality and sequence, the input data is valid for: %s" %
                    (", ".join(aggregator.get_valid_formats()) or "None"))
                ascii_range = aggregator.get_ascii_range()
                decimal_range = aggregator.get_decimal_range()
                # print using repr, since \x00 (null) causes info truncation in galaxy when printed
                print(
                    "Input ASCII range: %s(%i) - %s(%i)" %
                    (repr(ascii_range[0]), ord(ascii_range[0]), repr(ascii_range[1]), ord(ascii_range[1])))
                print("Input decimal range: %i - %i" % (decimal_range[0], decimal_range[1]))
        else:
            print("No valid FASTQ reads were provided.")

    def _get_args(self):
        types = ['solexa', 'illumina', 'sanger', 'cssanger']
        type_choices = [t + ext for t in types for ext in ['', '.gz', '.bz2']]
        fqe_choices = ['None', 'ascii', 'decimal']
        si_choices = ['summarize_input', 'dont_summarize_input']  # Should be yes/no (leave as is for now)

        p = argparse.ArgumentParser()
        p.add_argument('input_filename', help='file to groom')
        p.add_argument('input_type', choices=type_choices, help='input FASTQ quality scores type')
        p.add_argument('output_filename', help='groomed output file')
        p.add_argument('output_type', choices=type_choices, help='input FASTQ quality scores type')
        p.add_argument('force_quality_encoding', choices=fqe_choices, help='force quality score encoding')
        p.add_argument('summarize_input', choices=si_choices, help='summarize input data')

        fi_group = p.add_mutually_exclusive_group()
        fi_group.add_argument(
            '--fix-id', dest='fix_id', action='store_true', help='fix inconsistent identifiers')
        fi_group.add_argument(
            '--no-fix-id', dest='fix_id', action='store_false', help='do not fix inconsistent identifiers')
        p.set_defaults(fix_id=True)

        return p.parse_args()


def main():
    Groomer().run()


if __name__ == "__main__":
    main()
