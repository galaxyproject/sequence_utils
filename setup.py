from setuptools import setup, find_packages
setup( name="galaxy_sequence_utils",
       version="1.0.0",
       packages=find_packages('lib'),
       package_dir={ '': 'lib' },
       setup_requires=[],
       author="Dave Bouvier",
       author_email="dave@bx.psu.edu",
       description="Galaxy utilities for manipulating sequences.",
       url="http://galaxyproject.org",
       zip_safe=False,
       dependency_links=[] )
