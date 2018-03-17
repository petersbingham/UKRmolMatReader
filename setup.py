# -*- coding: utf-8 -*-

from distutils.core import setup
import shutil
shutil.copy('README.md', 'UKRmolMatReader/README.md')

setup(name='UKRmolMatReader',
      version='0.5',
      description='Python package to read K-matrix files produced by the UKRmol software.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['UKRmolMatReader'],
      package_data={'UKRmolMatReader': ['tests/*', 'README.md'],
     )
