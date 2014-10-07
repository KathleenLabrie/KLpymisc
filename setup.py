from setuptools import setup, find_packages
from codecs import open
import os

import klpymisc
VERSION = klpymisc.__version__

cwd = os.path.abspath(os.path.dirname(__file__))

# Get the long_description from the Description.rst file
with open(os.path.join(cwd, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

MODULENAME = 'klpymisc'

DATA_FILES = []
DOC_FILES = [(os.path.join('share',MODULENAME,root), [os.path.join(root,f) for f in files]) \
              for root, dirs, files in os.walk('docs')]
DATA_FILES.extend(DOC_FILES)

setup(
      name = MODULENAME,
      version = VERSION,
      
      description = 'Scientific Python utilities and tools',
      long_description = long_description,
      
      url = 'https://github.com/KathleenLabrie/KLpymisc',
      
      author = 'Kathleen Labrie',
      author_email = 'kathleen.labrie.phd@gmail.com',
      
      license = 'LICENSE',
      
      # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers = [
                    'Development Status :: 2 - Pre-Alpha',
                    'Intended Audience :: Science/Research',
                    'License :: OSI Approved :: ISC License (ISCL)',
                    'Operating System :: Mac OS :: MacOS X',
                    'Operating System :: POSIX :: Linux',
                    'Programming Language :: Python :: 2.7',
                    'Topic :: Scientific/Engineering :: Astronomy'
                    ],
      
      keywords = 'mathematics physics data processing',
      
      packages = find_packages(exclude=['docs']),
      
      #install_requires = ['']
      #extras_require = {
      #  'dev': [''],
      #},
      
      #package_data = {
      #                 'klpymisc': [''],
      #                },
      
      data_files = DATA_FILES,
      
      scripts = [
                 'klpymisc/admin/scripts/omniplan2alloc.py'
                 ],
      
      zip_safe = False,
      )
