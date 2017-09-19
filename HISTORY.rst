.. :changelog:

History
-------

.. to_doc

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
* Move wrapper scripts for Galaxy tools into this project and install as part of setup.py.
  `Pull Request 11`_

---------------------
1.0.2 (2017-02-02)
---------------------

* Apply common galaxyproject template to Python structure. 5e9bfc0_
* Merge in PEP-8 and Python 3 fixes from the core Galaxy project thanks to @nsoranzo.
  `Pull Request 4`_
* Implement project testings. a9b907c_
* First release published to PyPI.

---------------------
1.0.1 (2015-12-10)
---------------------

* Allow fastqJoiner to accept a string of bases to use between joined pairs.
  `Pull Request 3`_

---------------------
1.0.0 (2015-10-30)
---------------------

* Initial import extracted from Galaxy to build stand-alone dependencies for the tools in the Tool Shed.


https://github.com/galaxyproject/sequence_utils/pull/2

.. github_links
.. _a9b907c: https://github.com/galaxyproject/sequence_utils/commit/a9b907c
.. _c68932a: https://github.com/galaxyproject/sequence_utils/commit/c68932a
.. _5e9bfc0: https://github.com/galaxyproject/sequence_utils/commit/5e9bfc0
.. _Pull Request 4: https://github.com/galaxyproject/sequence_utils/pull/4
.. _Pull Request 3: https://github.com/galaxyproject/sequence_utils/pull/3
.. _Pull Request 11: https://github.com/galaxyproject/sequence_utils/pull/11
.. _Pull Request 13: https://github.com/galaxyproject/sequence_utils/pull/13
.. _Pull Request 14: https://github.com/galaxyproject/sequence_utils/pull/14
