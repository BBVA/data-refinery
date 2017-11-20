# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

Data refinery setup

"""
from setuptools import setup, find_packages
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(BASE_DIR, 'README.rst')) as f:
    README = f.read()

setup(name='data-refinery',
      python_requires='>=3.5',
      version=__import__('datarefinery').VERSION,
      description="Data Refinery: transformating data",
      author_email=["cesar.gallego@bbva.com ", "leticia.garcia3@bbva.com"],
      maintainer_email="cesar.gallego@bbva.com",
      license="Apache 2.0",
      long_description=README,
      classifiers=[
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Information Analysis'
      ],
      author='BBVA',
      url='https://github.com/BBVA/data-refinery',
      packages=find_packages(exclude=["tests", "docs"]),
      include_package_data=True,
      zip_safe=False)
