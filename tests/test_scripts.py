import contextlib
import os
import shutil
import sys

from tempfile import mkdtemp

from galaxy_utils.sequence.scripts import (
    fastq_to_tabular,
)

TEST_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = TEST_DIR


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


def _assert_paths_equal(actual, expected):
    with open(actual, "r") as f:
        actual_contents = f.read()

    with open(expected, "r") as f:
        expected_contents = f.read()

    assert actual_contents == expected_contents


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
