|Build Status| |Coverage| |Docs| |Version| |PyVersions| |License|

Data Refinery
=============

The main goal of the library is perform a Transformation over a data
event. Supports a variety of functions typically used on machine
learning and AI.

Development is oriented into a functional style avoiding side effects on
transformations.


Installation
------------

In console ``pip install data-refinery`` or ``python setup.py install`` from sources.

Usage example
-------------

.. code-block:: python

    from datarefinery.TupleOperations import wrap, keep, substitution
    from datarefinery.CombineOperations import sequential

    x2 = wrap(lambda x: x*2)

    operation = sequential(keep(["name"]), substitution(["value"], x2))
    (res, err) = operation({"name": "John", "value": 10})
    print(res) # {"name": "John", "value": 20}


Documentation
-------------

Visit complete documentation at `readthedocs.io <https://data-refinery.readthedocs.io>`_.


Compatibility
-------------

Python: 3.5, 3.6


Contribute
----------

Follow the steps on the `how to contribute <https://github.com/BBVA/data-refinery/blob/master/CONTRIBUTING.md>`_ document.

.. |Build Status| image:: https://travis-ci.org/BBVA/data-refinery.svg
   :target: https://travis-ci.org/BBVA/data-refinery
.. |Coverage| image:: https://codecov.io/gh/BBVA/data-refinery/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/BBVA/data-refinery
.. |Docs| image:: https://readthedocs.org/projects/data-refinery/badge/?version=latest
   :target: http://data-refinery.readthedocs.io/?badge=latest
.. |Version| image:: https://img.shields.io/pypi/v/data-refinery.svg
   :target: https://pypi.org/project/data-refinery
.. |PyVersions| image:: https://img.shields.io/pypi/pyversions/data-refinery.svg
   :target: https://pypi.org/project/data-refinery
.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0
