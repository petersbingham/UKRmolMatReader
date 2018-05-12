# -*- coding: utf-8 -*-

from distutils.core import setup
import shutil
shutil.copy('README.md', 'ukrmolmatreader/README.md')

setup(name='ukrmolmatreader',
      version='0.13',
      description='Python package to read K matrix files produced by https://ccpforge.cse.rl.ac.uk/gf/project/ukrmol-out/.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['ukrmolmatreader'],
      package_data={'ukrmolmatreader': ['tests/*', 'README.md']}
     )
