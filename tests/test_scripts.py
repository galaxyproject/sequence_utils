import contextlib
import os
import shutil
import sys
import unittest
from tempfile import mkdtemp

from galaxy_utils.sequence.fasta import fastaReader
from galaxy_utils.sequence.fastq import fastqReader
from galaxy_utils.sequence.scripts import (
    fastq_combiner,
    fastq_groomer,
    fastq_masker_by_quality,
    fastq_paired_end_deinterlacer,
    fastq_paired_end_interlacer,
    fastq_paired_end_joiner,
    fastq_paired_end_splitter,
    fastq_stats,
    fastq_to_tabular,
    fastq_trimmer_by_quality,
)
from galaxy_utils.sequence.scripts.fastq_groomer import Groomer
from galaxy_utils.sequence.vcf import Reader as vcfReader

TEST_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = TEST_DIR


class FastqGroomerTestCase(unittest.TestCase):

    def test_args_all(self):
        args = ['i_file', 'sanger', 'o_file', 'sanger.gz', 'ascii', 'summarize_input', '--fix-id']
        with _new_argv(args):
            g = Groomer()
            self.assertEqual('i_file', g.input_filename)
            self.assertEqual('sanger', g.input_type)
            self.assertEqual('o_file', g.output_filename)
            self.assertEqual('sanger.gz', g.output_type)
            self.assertEqual('ascii', g.force_quality_encoding)
            self.assertTrue(g.summarize_input)
            self.assertTrue(g.fix_id)

    def test_args_force_qual_enc_none(self):
        args = ['i_file', 'sanger', 'o_file', 'sanger.gz', 'None', 'summarize_input', '--fix-id']
        with _new_argv(args):
            g = Groomer()
            self.assertIsNone(g.force_quality_encoding)

    def test_args_input_type_illegal_choice(self):
        args = ['i_file', 'ILLEGAL', 'o_file', 'sanger.gz', 'None', 'summarize_input', '--fix-id']
        with _new_argv(args):
            with self.assertRaises(SystemExit):
                Groomer()

    def test_args_output_type_illegal_choice(self):
        args = ['i_file', 'sanger', 'o_file', 'ILLEGAL', 'None', 'summarize_input', '--fix-id']
        with _new_argv(args):
            with self.assertRaises(SystemExit):
                Groomer()

    def test_args_force_qual_enc_illegal_choice(self):
        args = ['i_file', 'sanger', 'o_file', 'sanger.gz', 'ILLEGAL', 'summarize_input', '--fix-id']
        with _new_argv(args):
            with self.assertRaises(SystemExit):
                Groomer()

    def test_args_summarize_imput_illegal_choice(self):
        args = ['i_file', 'sanger', 'o_file', 'sanger.gz', 'None', 'ILLEAGAL', '--fix-id']
        with _new_argv(args):
            with self.assertRaises(SystemExit):
                Groomer()

    def test_args_fixid_default(self):
        args = ['i_file', 'sanger', 'o_file', 'sanger.gz', 'None', 'summarize_input']
        with _new_argv(args):
            g = Groomer()
            self.assertTrue(g.fix_id)

    def test_args_fixid_yes(self):
        args = ['i_file', 'sanger', 'o_file', 'sanger.gz', 'None', 'summarize_input', '--fix-id']
        with _new_argv(args):
            g = Groomer()
            self.assertTrue(g.fix_id)

    def test_args_fixid_no(self):
        args = ['i_file', 'sanger', 'o_file', 'sanger.gz', 'None', 'summarize_input', '--no-fix-id']
        with _new_argv(args):
            g = Groomer()
            self.assertFalse(g.fix_id)


def test_fix_inconsistent_id():
    i_path = _data_path('test_data/fastqreader_min_invalid-line3')
    o_path = _data_path('test_data/fastqreader_min_invalid-line3_fixed')
    with _new_argv([i_path, "sanger", "output", "sanger", 'ascii', 'summarize_input', '--fix-id']):
        fastq_groomer.main()
        _assert_paths_equal("output", o_path)


def test_fasta_reader_cleanup():
    i_path = _data_path("fasta_reader_1.fasta")
    fh = open(i_path)
    with _new_argv([fh]):
        reader = fastaReader(fh)
        for _ in reader:
            pass
    assert(fh.closed)


def test_fastq_reader_cleanup():
    i_path = _data_path("sanger_full_range_original_sanger.fastqsanger")
    fh = open(i_path)
    with _new_argv([fh]):
        reader = fastqReader(fh)
        for _ in reader:
            pass
    assert(fh.closed)


def test_vcf_reader_cleanup():
    i_path = _data_path("vcf_reader_1.vcf")
    fh = open(i_path, "rt")
    with _new_argv([fh]):
        reader = vcfReader(fh)
        for _ in reader:
            pass
    assert(fh.closed)


def test_fastq_to_tabular():
    i_path = _data_path("sanger_full_range_original_sanger.fastqsanger")
    o_path = _data_path("fastq_to_tabular_out_1.tabular")
    with _new_argv([i_path, "output", "1", "sanger"]):
        fastq_to_tabular.main()
        _assert_paths_equal("output", o_path)


def test_fastq_to_tabular_gz():
    i_path = _data_path("sanger_full_range_original_sanger.fastqsanger.gz")
    o_path = _data_path("fastq_to_tabular_out_1.tabular")
    with _new_argv([i_path, "output", "1", "sanger.gz"]):
        fastq_to_tabular.main()
        _assert_paths_equal("output", o_path)


def test_fastq_to_tabular_bz2():
    i_path = _data_path("sanger_full_range_original_sanger.fastqsanger.bz2")
    o_path = _data_path("fastq_to_tabular_out_1.tabular")
    with _new_argv([i_path, "output", "1", "sanger.bz2"]):
        fastq_to_tabular.main()
        _assert_paths_equal("output", o_path)


def test_fastq_groomer_bz2():
    i_path = _data_path("sanger_full_range_original_sanger.fastqsanger.bz2")
    with _new_argv([i_path, "sanger.bz2", "output", "sanger.bz2", 'ascii', 'summarize_input']):
        fastq_groomer.main()
        _assert_paths_equal("output", i_path)


def test_fastq_combiner():
    fasta_path = _data_path("fastq_combiner_in_1.fasta")
    fastq_path = _data_path("fastq_combiner_no_qual_decimal_out_1.fastqsanger")
    with _new_argv([fasta_path, "fasta", "None", "qualsanger", "output", "decimal"]):
        fastq_combiner.main()
        _assert_paths_equal("output", fastq_path)


def test_fastq_trimmer_by_quality():
    i_path = _data_path("sanger_full_range_original_sanger.fastqsanger.bz2")
    o_path = _data_path("sanger_full_range_quality_trimmed_out_1.fastqsanger.bz2")
    with _new_argv([i_path, "output", "-f", "sanger.bz2", "-s", "1",
                    "-t", "1", "-e", "53", "-a", "min", "-x", "0", "-c", ">=", "-q", "20"]):
        fastq_trimmer_by_quality.main()
        _assert_paths_equal("output", o_path)


def test_fastq_masker_by_quality():
    i_path = _data_path("sanger_full_range_original_sanger.fastqsanger.bz2")
    o_path = _data_path("sanger_full_range_masked_N.fastqsanger.bz2")
    with _new_argv([i_path, "output", "-f", "sanger.bz2", "-s", "20", "-c", "le", "-m", "N"]):
        fastq_masker_by_quality.main()
        _assert_paths_equal("output", o_path)


def test_fastq_paired_end_joiner():
    i_1_path = _data_path("split_pair_reads_1.fastqsanger")
    i_2_path = _data_path("split_pair_reads_2.fastqsanger")
    o_path = _data_path("3.fastqsanger")
    with _new_argv([i_1_path, "sanger", i_2_path, "sanger", "output", "old", ""]):
        fastq_paired_end_joiner.main()
        _assert_paths_equal("output", o_path)


def test_fastq_paired_end_splitter():
    i_path = _data_path("3.fastqsanger")
    o_1_path = _data_path("split_pair_reads_1.fastqsanger")
    o_2_path = _data_path("split_pair_reads_2.fastqsanger")
    with _new_argv([i_path, "sanger", "output_1", "output_2"]):
        fastq_paired_end_splitter.main()
        _assert_paths_equal("output_1", o_1_path)
        _assert_paths_equal("output_2", o_2_path)


def test_fastq_paired_end_deinterlacer():
    i_path = _data_path("paired_end_merged_errors.fastqsanger")
    o_1_path = _data_path("paired_end_1_cleaned.fastqsanger")
    o_2_path = _data_path("paired_end_2_cleaned.fastqsanger")
    o_3_path = _data_path("paired_end_1_cleaned_singles.fastqsanger")
    o_4_path = _data_path("paired_end_2_cleaned_singles.fastqsanger")
    with _new_argv([i_path, "sanger", "o1", "o2", "o3", "o4"]):
        fastq_paired_end_deinterlacer.main()
        _assert_paths_equal("o1", o_1_path)
        _assert_paths_equal("o2", o_2_path)
        _assert_paths_equal("o3", o_3_path)
        _assert_paths_equal("o4", o_4_path)


def test_fastq_paired_end_interlacer():
    i_1_path = _data_path("paired_end_1_errors.fastqsanger")
    i_2_path = _data_path("paired_end_2_errors.fastqsanger")
    o_pairs_path = _data_path("paired_end_merged_cleaned.fastqsanger")
    o_singles_path = _data_path("paired_end_merged_cleaned_singles.fastqsanger")
    with _new_argv([i_1_path, "sanger", i_2_path, "sanger", "o_pairs", "o_singles"]):
        fastq_paired_end_interlacer.main()
        _assert_paths_equal("o_pairs", o_pairs_path)
        _assert_paths_equal("o_singles", o_singles_path)


def test_fastq_stats():
    i_path = _data_path("fastq_stats1.fastq")
    o_path = _data_path("fastq_stats_1_out.tabular")
    with _new_argv([i_path, "output", "sanger"]):
        fastq_stats.main()
        _assert_paths_equal("output", o_path)


def _assert_paths_equal(actual, expected):
    with open(actual, "rb") as f:
        actual_contents = f.read()

    with open(expected, "rb") as f:
        expected_contents = f.read()

    assert actual_contents == expected_contents, "%s != %s" % (actual_contents, expected_contents)


def _data_path(filename):
    path = os.path.join(TEST_DATA_DIR, filename)
    assert os.path.exists(path)
    return os.path.abspath(path)


@contextlib.contextmanager
def _new_argv(argv):
    o_argv = sys.argv
    o_cwd = os.getcwd()
    try:
        sys.argv = ["script"] + argv
        with _TempDirectoryContext() as temp_dir:
            try:
                os.chdir(temp_dir.temp_directory)
                yield temp_dir.temp_directory
            finally:
                os.chdir(o_cwd)
    finally:
        sys.argv = o_argv


class _TempDirectoryContext(object):

    def __init__(self):
        self.temp_directory = mkdtemp()

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        shutil.rmtree(self.temp_directory)
