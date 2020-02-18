.. :changelog:

History
-------

.. to_doc

---------------------
1.1.5 (2020-02-18)
---------------------

* Fix fastqreader file handling and CI tests `Pull Request 27`_

---------------------
1.1.4 (2020-02-07)
---------------------

* Drop support for Python < 3.5
  `Pull Request 24`_, `Pull Request 25`_
* Prevent ``StopIteration`` from raising ``RuntimeError``
  `Pull Request 20`_
* Add ``fastqReader`` tests+test data; refactor; modify
  `Pull Request 22`_
* Fix inconsistent identifier option for ``fastq_groomer``
  `Pull Request 23`_

---------------------
1.1.3 (2018-07-06)
---------------------

* Cope with default ``format=None`` in ``fastaWriter`` and ``fastqWriter``
  `Pull Request 16`_

---------------------
1.1.2 (2017-10-05)
---------------------

* Do not open compressed file twice in ``fastqNamedReader`` class
  `Pull Request 15`_

---------------------
1.1.1 (2017-09-19)
---------------------

* Fix fastq_filter.py , fastq_masker_by_quality.py , fastq_stats.py and
  fastq_to_fasta.py wrapper scripts
  `Pull Request 14`_
* Fix fastq_filter.py wrapper script
  `Pull Request 13`_

---------------------
1.1.0 (2017-02-13)
---------------------

* Support gz and bzip2 compressed files.
  `Pull Request 11`_
* Move wrapper scripts for Galaxy tools into this project and install as part of
  setup.py .
  `Pull Request 11`_

---------------------
1.0.2 (2017-02-02)
---------------------

* Apply common galaxyproject template to Python structure. 5e9bfc0_
* Merge in PEP-8 and Python 3 fixes from the core Galaxy project thanks to
  @nsoranzo.
  `Pull Request 4`_
* Implement project testings. a9b907c_
* First release published to PyPI.

---------------------
1.0.1 (2015-12-10)
---------------------

* Allow fastqJoiner to accept a string of bases to use between joined pairs.
  `Pull Request 2`_

---------------------
1.0.0 (2015-10-30)
---------------------

* Initial import extracted from Galaxy to build stand-alone dependencies for the
  tools in the Tool Shed.
* Use setuptools
  `Pull Request 1`_

.. github_links
.. _Pull Request 27: https://github.com/galaxyproject/sequence_utils/pull/27
.. _a9b907c: https://github.com/galaxyproject/sequence_utils/commit/a9b907c
.. _c68932a: https://github.com/galaxyproject/sequence_utils/commit/c68932a
.. _5e9bfc0: https://github.com/galaxyproject/sequence_utils/commit/5e9bfc0
.. _Pull Request 1: https://github.com/galaxyproject/sequence_utils/pull/1
.. _Pull Request 2: https://github.com/galaxyproject/sequence_utils/pull/2
.. _Pull Request 4: https://github.com/galaxyproject/sequence_utils/pull/4
.. _Pull Request 11: https://github.com/galaxyproject/sequence_utils/pull/11
.. _Pull Request 13: https://github.com/galaxyproject/sequence_utils/pull/13
.. _Pull Request 14: https://github.com/galaxyproject/sequence_utils/pull/14
.. _Pull Request 15: https://github.com/galaxyproject/sequence_utils/pull/15
.. _Pull Request 16: https://github.com/galaxyproject/sequence_utils/pull/16
.. _Pull Request 20: https://github.com/galaxyproject/sequence_utils/pull/20
.. _Pull Request 22: https://github.com/galaxyproject/sequence_utils/pull/22
.. _Pull Request 23: https://github.com/galaxyproject/sequence_utils/pull/23
.. _Pull Request 24: https://github.com/galaxyproject/sequence_utils/pull/24
.. _Pull Request 25: https://github.com/galaxyproject/sequence_utils/pull/25
