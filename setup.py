#! /usr/bin/env python

"""
The oemof_examples repository holds a collections of various examples
on how to build an energy system with different versions of oemof.

Install the required packages for the oemof version you want to use by
`pip install -e <path/to/package>['oemof/version']`, e.g.
`pip install -e oemof_examples/['oemof_0.2']`.

If you want to run a jupyter notebook add `jupyter` to the pip call, e.g.
`pip install -e oemof_examples/['oemof_0.2, jupyter']`.

"""

from setuptools import find_packages, setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='oemof_examples',
      version='0.0.1',
      license='GNU General Public License v3.0',
      author='oemof developer group',
      author_email='',
      description='Collection of oemof examples',
      url='https://oemof.org/',
      long_description=read('README.rst'),
      packages=find_packages(),
      install_requires=['matplotlib'],
      extras_require={
          'oemof_0.1': ["oemof>=0.1.0, <=0.1.4"],
          'oemof_0.2': ["oemof >= 0.2.0"],
          'jupyter': ["jupyter"]})
