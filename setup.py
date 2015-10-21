import sys

if sys.version_info < (2, 6):
    print >> sys.stderr, "ERROR: galaxy_sequence_utils requires python 2.6 or greater"
    sys.exit()

# Automatically download setuptools if not available
from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages
from glob import glob

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

       
def main():
    setup(  name = "galaxy_sequence_utils",
            version = "1.0.0",
            packages = find_packages( 'lib' ),
            package_dir = { '': 'lib' },
            scripts = glob( "scripts/*.py" ),
            setup_requires = [],
            author = "Dave Bouvier",
            author_email = "dave@bx.psu.edu",
            description = "Galaxy utilities for manipulating sequences.",
            url = "http://galaxyproject.org",
            zip_safe = False,
            dependency_links = [],
            **extra )

if __name__ == "__main__":
    main()