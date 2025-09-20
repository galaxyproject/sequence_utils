import os
import unittest

from galaxy_utils.sequence.fastq import (
    fastqFormatError,
    fastqReader,
)

TEST_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.join(TEST_DIR, 'test_data')


class FastqReaderTestCase(unittest.TestCase):

    def test_file_closed_on_completion(self):
        i_path = _data_path('fastqreader_min')
        fh = open(i_path)
        with fastqReader(fh) as reader:
            for _ in reader:
                pass

        self.assertTrue(
            fh.closed,
            'File should be closed after iteration compeletes')

    def test_file_closed_on_header_error(self):
        i_path = _data_path('fastqreader_min_invalid-header')
        fh = open(i_path)

        with fastqReader(fh) as reader:
            with self.assertRaises(fastqFormatError):
                for _ in reader:
                    pass

        self.assertTrue(
            fh.closed,
            'File should be closed if exception occurs due to invalid header')

    def test_invalid_header(self):
        i_path = _data_path('fastqreader_min_invalid-header')

        with fastqReader(path=i_path) as reader:
            with self.assertRaises(fastqFormatError):
                for _ in reader:
                    pass

    def test_read_header(self):
        i_path = _data_path('fastqreader_min')
        with fastqReader(path=i_path) as reader:
            rvals = [rval for rval in reader]

        expected_reads = 2
        expected_headers = '@FAKE-1', '@FAKE-2'

        self.assertEqual(expected_reads, len(rvals))
        self.assertEqual(expected_headers[0], rvals[0].identifier)
        self.assertEqual(expected_headers[1], rvals[1].identifier)

    def test_read_sequence(self):
        i_path = _data_path('fastqreader_min')
        with fastqReader(path=i_path) as reader:
            rvals = [rval for rval in reader]

        expected_reads = 2
        expected_seqs = 'ACGTACGTAC', 'CATGCATGCA'

        self.assertEqual(expected_reads, len(rvals))
        self.assertEqual(expected_seqs[0], rvals[0].get_sequence())
        self.assertEqual(expected_seqs[1], rvals[1].get_sequence())

    def test_read_sequence_multiline(self):
        i_path = _data_path('fastqreader_min-multiline')
        with fastqReader(path=i_path) as reader:
            rvals = [rval for rval in reader]

        expected_reads = 2
        expected_seqs = 'ACGTACGTACGTACGTACGT', 'CATGCATGCATGCATGCATG'

        self.assertEqual(expected_reads, len(rvals))
        self.assertEqual(expected_seqs[0], rvals[0].get_sequence())
        self.assertEqual(expected_seqs[1], rvals[1].get_sequence())

    def test_read_qualityscores(self):
        i_path = _data_path('fastqreader_min')
        with fastqReader(path=i_path) as reader:
            rvals = [rval for rval in reader]

        expected_reads = 2
        expected_scores = '!##$%&&()*', '~}|{zyxwvu'

        self.assertEqual(expected_reads, len(rvals))
        self.assertEqual(expected_scores[0], rvals[0].quality)
        self.assertEqual(expected_scores[1], rvals[1].quality)

    def test_read_qualityscores_multiline(self):
        i_path = _data_path('fastqreader_min-multiline')
        with fastqReader(path=i_path) as reader:
            rvals = [rval for rval in reader]

        expected_reads = 2
        expected_scores = '!##$%&&()**,-./01234', '~}|{zyxwvutsrqponmlk'

        self.assertEqual(expected_reads, len(rvals))
        self.assertEqual(expected_scores[0], rvals[0].quality)
        self.assertEqual(expected_scores[1], rvals[1].quality)

    def test_read_qualityscores_edgecase_multiline(self):
        # Quality score input designed to confuse the parser
        i_path = _data_path('fastqreader_min-multiline-edgecase')
        with fastqReader(path=i_path) as reader:
            rvals = [rval for rval in reader]

        expected_reads = 2
        expected_scores = ('+##$%&&()*+##$%&&()*@,-./01234', '@}|{zyxwvu@}|{zyxwvu+srqponmlk')

        self.assertEqual(expected_reads, len(rvals))
        self.assertEqual(expected_scores[0], rvals[0].quality)
        self.assertEqual(expected_scores[1], rvals[1].quality)

    def test_read_line3(self):
        # Separate test case for line3 containing a copy of line1
        i_path = _data_path('fastqreader_min-line3')
        with fastqReader(path=i_path) as reader:
            rvals = [rval for rval in reader]

        expected_reads = 2
        expected_seqs = 'ACGTACGTAC', 'CATGCATGCA'
        expected_scores = '!##$%&&()*', '~}|{zyxwvu'

        self.assertEqual(expected_reads, len(rvals))
        for i in range(len(rvals)):
            self.assertEqual(expected_scores[i], rvals[i].quality)
            self.assertEqual(expected_seqs[i], rvals[i].get_sequence())

    def test_invalid_line3(self):
        i_path = _data_path('fastqreader_min_invalid-line3')
        with fastqReader(path=i_path) as reader:
            with self.assertRaises(fastqFormatError):
                for _ in reader:
                    pass

    def test_file_closed_on_line3_error(self):
        i_path = _data_path('fastqreader_min_invalid-line3')
        fh = open(i_path)
        with fastqReader(fh) as reader:
            with self.assertRaises(fastqFormatError):
                for _ in reader:
                    pass
        self.assertTrue(
            fh.closed,
            'File should be closed if exception occurs due to invalid line3')

    def test_invalid_line3_stripped(self):
        i_path = _data_path('fastqreader_min_invalid-line3')
        # fix_id=True: fix inconsistent identifiers (source: SRA data dumps)k
        with fastqReader(path=i_path, fix_id=True) as reader:
            rvals = [rval for rval in reader]

        expected_reads = 2
        expected_seqs = 'ACGTACGTAC', 'CATGCATGCA'
        expected_scores = '!##$%&&()*', '~}|{zyxwvu'
        expected_line3 = '+'

        self.assertEqual(expected_reads, len(rvals))
        for i in range(len(rvals)):
            self.assertEqual(expected_scores[i], rvals[i].quality)
            self.assertEqual(expected_seqs[i], rvals[i].get_sequence())
            self.assertEqual(expected_line3, rvals[i].description)


def _data_path(filename):
    path = os.path.join(TEST_DATA_DIR, filename)
    assert os.path.exists(path)
    return os.path.abspath(path)
