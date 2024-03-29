"""
Extended version of Dan Blankenberg's fastq joiner ( adds support for
recent Illumina headers ).
"""

import re
import sys

import galaxy_utils.sequence.fastq as fq


class IDManager:

    def __init__(self, sep="\t"):
        """
        Recent Illumina FASTQ header format::

          @<COORDS> <FLAGS>
          COORDS = <Instrument>:<Run #>:<Flowcell ID>:<Lane>:<Tile>:<X>:<Y>
          FLAGS = <Read>:<Is Filtered>:<Control Number>:<Index Sequence>

        where the whitespace character between <COORDS> and <FLAGS> can be
        either a space or a tab.
        """
        self.sep = sep

    def parse_id(self, identifier):
        try:
            coords, flags = identifier.strip()[1:].split(self.sep, 1)
        except ValueError:
            raise RuntimeError(f"bad identifier: {identifier!r}")
        return coords.split(":"), flags.split(":")

    def join_id(self, parsed_id):
        coords, flags = parsed_id
        return f'@{":".join(coords)}{self.sep}{":".join(flags)}'

    def get_read_number(self, parsed_id):
        return int(parsed_id[1][0])

    def set_read_number(self, parsed_id, n):
        parsed_id[1][0] = f"{n:d}"

    def get_paired_identifier(self, read):
        t = self.parse_id(read.identifier)
        n = self.get_read_number(t)
        if n == 1:
            pn = 2
        elif n == 2:
            pn = 1
        else:
            raise RuntimeError(f"Unknown read number '{n:d}'")
        self.set_read_number(t, pn)
        return self.join_id(t)


class FastqJoiner(fq.fastqJoiner):

    def __init__(self, format, force_quality_encoding=None, sep="\t", paste=""):
        super().__init__(format, force_quality_encoding, paste=paste)
        self.id_manager = IDManager(sep)

    def join(self, read1, read2):
        force_quality_encoding = self.force_quality_encoding
        if not force_quality_encoding:
            if read1.is_ascii_encoded():
                force_quality_encoding = 'ascii'
            else:
                force_quality_encoding = 'decimal'
        read1 = read1.convert_read_to_format(self.format, force_quality_encoding=force_quality_encoding)
        read2 = read2.convert_read_to_format(self.format, force_quality_encoding=force_quality_encoding)
        # --
        t1, t2 = (self.id_manager.parse_id(r.identifier) for r in (read1, read2))
        if self.id_manager.get_read_number(t1) == 2:
            if not self.id_manager.get_read_number(t2) == 1:
                raise RuntimeError("input files are not from mated pairs")
            read1, read2 = read2, read1
            t1, t2 = t2, t1
        # --
        rval = fq.FASTQ_FORMATS[self.format]()
        rval.identifier = read1.identifier
        rval.description = "+"
        if len(read1.description) > 1:
            rval.description += rval.identifier[1:]
        if rval.sequence_space == 'color':
            # convert to nuc space, join, then convert back
            rval.sequence = rval.convert_base_to_color_space(
                read1.convert_color_to_base_space(read1.sequence) + self.paste_sequence
                + read2.convert_color_to_base_space(read2.sequence)
            )
        else:
            rval.sequence = read1.sequence + self.paste_sequence + read2.sequence
        if force_quality_encoding == 'ascii':
            rval.quality = read1.quality + self.paste_ascii_quality + read2.quality
        else:
            rval.quality = f"{read1.quality.strip()} {self.paste_decimal_quality}"
            rval.quality = f"{rval.quality.strip()} {read2.quality.strip()}".strip()
        return rval

    def get_paired_identifier(self, read):
        return self.id_manager.get_paired_identifier(read)


def sniff_sep(fastq_fn):
    header = ""
    with open(fastq_fn) as f:
        while header == "":
            try:
                header = f.next().strip()
            except StopIteration:
                raise RuntimeError(f"{fastq_fn!r}: empty file")
    return re.search(r"\s", header).group()


def main():
    # Read command line arguments
    input1_filename = sys.argv[1]
    input1_type = sys.argv[2] or 'sanger'
    input2_filename = sys.argv[3]
    input2_type = sys.argv[4] or 'sanger'
    output_filename = sys.argv[5]

    fastq_style = sys.argv[6] or 'old'

    paste = sys.argv[7] or ''
    # --
    if input1_type != input2_type:
        print(f"WARNING: You are trying to join files of two different types: {input1_type} and {input2_type}.")

    if fastq_style == 'new':
        sep = sniff_sep(input1_filename)
        joiner = FastqJoiner(input1_type, sep=sep, paste=paste)
    else:
        joiner = fq.fastqJoiner(input1_type, paste=paste)
    # --
    i = None
    skip_count = 0

    writer = fq.fastqWriter(path=output_filename, format=input1_type)
    reader1 = fq.fastqReader(path=input1_filename, format=input1_type)
    reader2 = fq.fastqNamedReader(path=input2_filename, format=input2_type)

    with writer, reader1, reader2:
        for i, fastq_read in enumerate(reader1):
            identifier = joiner.get_paired_identifier(fastq_read)
            fastq_paired = reader2.get(identifier)
            if fastq_paired is None:
                skip_count += 1
            else:
                writer.write(joiner.join(fastq_read, fastq_paired))

        # this indent is correct: we still need access to reader2
        if i is None:
            print("Your file contains no valid FASTQ reads.")
        else:
            print(reader2.has_data())
            print(f'Joined {i - skip_count + 1} of {i + 1} read pairs ({(i - skip_count + 1) / (i + 1) * 100.0:.2f}%).')


if __name__ == "__main__":
    main()
