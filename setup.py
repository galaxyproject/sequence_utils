#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

SOURCE_DIR = "galaxy_utils"

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('%s/__init__.py' % SOURCE_DIR, 'rb') as f:
    init_contents = f.read().decode('utf-8')

    def get_var(var_name):
        pattern = re.compile(r'%s\s+=\s+(.*)' % var_name)
        match = pattern.search(init_contents).group(1)
        return str(ast.literal_eval(match))

    version = get_var("__version__")
    PROJECT_NAME = get_var("PROJECT_NAME")
    PROJECT_URL = get_var("PROJECT_URL")
    PROJECT_AUTHOR = get_var("PROJECT_AUTHOR")
    PROJECT_EMAIL = get_var("PROJECT_EMAIL")

TEST_DIR = 'tests'
PROJECT_DESCRIPTION = 'Galaxy utilities for manipulating sequences Galaxy project.'
PACKAGES = [
    'galaxy_utils',
    'galaxy_utils.sequence',
    'galaxy_utils.sequence.scripts',
]
ENTRY_POINTS = '''
        [console_scripts]
        gx-fastq-to-tabular=galaxy_utils.sequence.scripts.fastq_to_tabular:main
        gx-fastq-groomer=galaxy_utils.sequence.scripts.fastq_groomer:main
        gx-fastq-combiner=galaxy_utils.sequence.scripts.fastq_combiner:main
        gx-fastq-filter=galaxy_utils.sequence.scripts.fastq_filter:main
        gx-fastq-manipulation=galaxy_utils.sequence.scripts.fastq_manipulation:main
        gx-fastq-masker-by-quality=galaxy_utils.sequence.scripts.fastq_masker_by_quality:main
        gx-fastq-paired-end-deinterlacer=galaxy_utils.sequence.scripts.fastq_paired_end_deinterlacer:main
        gx-fastq-paired-end-interlacer=galaxy_utils.sequence.scripts.fastq_paired_end_interlacer:main
        gx-fastq-paired-end-joiner=galaxy_utils.sequence.scripts.fastq_paired_end_joiner:main
        gx-fastq-paired-end-splitter=galaxy_utils.sequence.scripts.fastq_paired_end_splitter:main
        gx-fastq-stats=galaxy_utils.sequence.scripts.fastq_stats:main
        gx-fastq-to-fasta=galaxy_utils.sequence.scripts.fastq_to_fasta:main
        gx-fastq-trimmer=galaxy_utils.sequence.scripts.fastq_trimmer:main
        gx-fastq-trimmer-by-quality=galaxy_utils.sequence.scripts.fastq_trimmer_by_quality:main
'''
PACKAGE_DATA = {}
PACKAGE_DIR = {
    SOURCE_DIR: SOURCE_DIR,
}

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

if os.path.exists("requirements.txt"):
    requirements = open("requirements.txt").read().split("\n")
else:
    # In tox, it will cover them anyway.
    requirements = []
test_requirements = []


setup(
    name=PROJECT_NAME,
    version=version,
    description=PROJECT_DESCRIPTION,
    long_description=readme + '\n\n' + history,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    url=PROJECT_URL,
    packages=PACKAGES,
    entry_points=ENTRY_POINTS,
    package_data=PACKAGE_DATA,
    package_dir=PACKAGE_DIR,
    include_package_data=True,
    install_requires=requirements,
    license="AFL",
    zip_safe=False,
    keywords='planemo',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'License :: OSI Approved :: Academic Free License (AFL)',
        'Operating System :: POSIX',
        'Topic :: Software Development',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite=TEST_DIR,
    tests_require=test_requirements
)
