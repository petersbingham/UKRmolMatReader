# -*- coding: utf-8 -*-

from distutils.core import setup
import os
import shutil
shutil.copy('README.md', 'ukrmolmatreader/README.md')

dir_setup = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_setup, 'ukrmolmatreader', 'release.py')) as f:
    # Defines __version__
    exec(f.read())

setup(name='ukrmolmatreader',
      version=__version__,
      description='Python package to read K matrix files produced by https://ccpforge.cse.rl.ac.uk/gf/project/ukrmol-out/.',
      author="Peter Bingham",
      author_email="petersbingham@hotmail.co.uk",
      packages=['ukrmolmatreader'],
      package_data={'ukrmolmatreader': ['tests/*', 'README.md']}
     )
