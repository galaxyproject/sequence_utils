# Dan Blankenberg
import bz2
import gzip


class fastaSequence:
    def __init__(self):
        self.identifier = None
        self.sequence = ''  # holds raw sequence string: no whitespace

    def __len__(self):
        return len(self.sequence)

    def __str__(self):
        return f"{self.identifier}\n{self.sequence}\n"


class fastaReader:
    def __init__(self, fh):
        self.file = fh

    def close(self):
        return self.file.close()

    def __next__(self):
        line = self.file.readline()
        # remove header comment lines
        while line and line.startswith('#'):
            line = self.file.readline()
        if not line:
            raise StopIteration
        assert line.startswith('>'), "FASTA headers must start with >"
        rval = fastaSequence()
        rval.identifier = line.strip()
        offset = self.file.tell()
        while True:
            line = self.file.readline()
            if not line or line.startswith('>'):
                if line:
                    self.file.seek(offset)  # this causes sequence id lines to be read twice, once to determine previous sequence end and again when getting actual sequence; can we cache this to prevent it from being re-read?
                return rval
            # 454 qual test data that was used has decimal scores that don't have trailing spaces
            # so we'll need to parse and build these sequences not based upon de facto standards
            # i.e. in a less than ideal fashion
            line = line.rstrip()
            if ' ' in rval.sequence or ' ' in line:
                rval.sequence = f"{rval.sequence}{line} "
            else:
                rval.sequence += line
            offset = self.file.tell()

    def __iter__(self):
        while True:
            try:
                yield next(self)
            except StopIteration:
                self.close()
                # Catch exception and return normally
                return


class fastaNamedReader:
    def __init__(self, fh):
        self.file = fh
        self.reader = fastaReader(self.file)
        self.offset_dict = {}
        self.eof = False

    def close(self):
        return self.file.close()

    def get(self, sequence_id):
        if not isinstance(sequence_id, str):
            sequence_id = sequence_id.identifier
        rval = None
        if sequence_id in self.offset_dict:
            initial_offset = self.file.tell()
            seq_offset = self.offset_dict[sequence_id].pop(0)
            if not self.offset_dict[sequence_id]:
                del self.offset_dict[sequence_id]
            self.file.seek(seq_offset)
            rval = next(self.reader)
            self.file.seek(initial_offset)
        else:
            while True:
                offset = self.file.tell()
                try:
                    fasta_seq = next(self.reader)
                except StopIteration:
                    self.eof = True
                    break  # eof, id not found, will return None
                if fasta_seq.identifier == sequence_id:
                    rval = fasta_seq
                    break
                else:
                    if fasta_seq.identifier not in self.offset_dict:
                        self.offset_dict[fasta_seq.identifier] = []
                    self.offset_dict[fasta_seq.identifier].append(offset)
        return rval

    def has_data(self):
        # returns a string representation of remaining data, or empty string (False) if no data remaining
        eof = self.eof
        count = 0
        rval = ''
        if self.offset_dict:
            count = sum(map(len, self.offset_dict.values()))
        if not eof:
            offset = self.file.tell()
            try:
                next(self.reader)
            except StopIteration:
                eof = True
            self.file.seek(offset)
        if count:
            rval = f"There were {count:d} known sequences not utilized. "
        if not eof:
            rval += "An additional unknown number of sequences exist in the input that were not utilized."
        return rval


class fastaWriter:
    def __init__(self, fh=None, format=None, path=None):
        if fh is None:
            assert path is not None
            if format and format.endswith(".gz"):
                fh = gzip.open(path, "wt")
            elif format and format.endswith(".bz2"):
                fh = bz2.open(path, mode="wt")
            else:
                fh = open(path, "w")
        else:
            if format and format.endswith(".gz"):
                fh = gzip.GzipFile(fileobj=fh)
            elif format and format.endswith(".bz2"):
                raise Exception("bz2 formats do not support file handle inputs")
        self.file = fh

    def write(self, fasta_read):
        # this will include color space adapter base if applicable
        self.file.write(f">{fasta_read.identifier[1:]}\n{fasta_read.sequence}\n")

    def close(self):
        return self.file.close()
