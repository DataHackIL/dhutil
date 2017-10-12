dhutil
#########
|PyPI-Status| |PyPI-Versions| |Build-Status| |Codecov| |LICENCE|

A small pure-python package for data dhutilure related utility functions.

.. code-block:: python

  from dhutil.dict import get_nested_val

  >>> dict_obj = {'a': {'b': 7}}
  >>> get_nested_val(('a', 'b'), dict_obj)
  7

.. contents::

.. section-numbering::


Installation
============

Install ``dhutil`` with:

.. code-block:: bash

  pip install dhutil


Use
===

``dhutil`` is divided into four sub-modules.

dict
----

Getting values from nested dicts in various ways; operations on number-valued dicts; merging, normalizing, reversing and printing dicts (nicely)


list
----

Index and element shifts that preserve order.


set
---

Getting a set element by a priority list.


sortedlist
----------

Operations on sortedcontainers.SortedList objects.


Contributing
============

Package author and current maintainer is Shay Palachy (shay.palachy@gmail.com); You are more than welcome to approach him for help. Contributions are very welcomed.

Installing for development
--------------------------

Clone:

.. code-block:: bash

  git clone git@github.com:shaypal5/dhutil.git


Install in development mode with test dependencies:

.. code-block:: bash

  cd dhutil
  pip install -e ".[test]"


Running the tests
-----------------

To run the tests, use:

.. code-block:: bash

  python -m pytest --cov=dhutil --doctest-modules


Adding documentation
--------------------

This project is documented using the `numpy docstring conventions`_, which were chosen as they are perhaps the most widely-spread conventions that are both supported by common tools such as Sphinx and result in human-readable docstrings (in my personal opinion, of course). When documenting code you add to this project, please follow `these conventions`_.

.. _`numpy docstring conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt
.. _`these conventions`: https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt


Credits
=======
Created by Shay Palachy  (shay.palachy@gmail.com).

.. |PyPI-Status| image:: https://img.shields.io/pypi/v/dhutil.svg
  :target: https://pypi.python.org/pypi/dhutil

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/dhutil.svg
   :target: https://pypi.python.org/pypi/dhutil

.. |Build-Status| image:: https://travis-ci.org/shaypal5/dhutil.svg?branch=master
  :target: https://travis-ci.org/shaypal5/dhutil

.. |LICENCE| image:: https://img.shields.io/pypi/l/dhutil.svg
  :target: https://pypi.python.org/pypi/dhutil

.. |Codecov| image:: https://codecov.io/github/shaypal5/dhutil/coverage.svg?branch=master
   :target: https://codecov.io/github/shaypal5/dhutil?branch=master
