|Build Status| |Coverage| |Docs|

ETL library
===========

The main goal of the library is perform a Transformation over a data
event. Supports a variety of functions typically used on machine
learning and AI.

Development is oriented into a functional style avoiding side effects on
transformations. This code is inspired by parser combinator libraries;
that use for each function only one input (in order to chain functions)
and two output (output or error).

Installation
------------

-  In console ``pip install data-refinery`` or ``python setup.py install`` from sources.

.. |Build Status| image:: https://travis-ci.org/BBVA/data-refinery.svg
   :target: https://travis-ci.org/BBVA/data-refinery
.. |Coverage| image:: https://codecov.io/gh/BBVA/data-refinery/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/BBVA/data-refinery
.. |Docs| image:: https://readthedocs.org/projects/data-refinery/badge/?version=latest
   :target: http://data-refinery.readthedocs.io/?badge=latest