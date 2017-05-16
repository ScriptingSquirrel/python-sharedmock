Python ``SharedMock``
=====================

|Build Status| |Coverage Status| |Docs Status|

.. |Build Status| image:: https://travis-ci.org/elritsch/python-sharedmock.svg?branch=master
   :target: https://travis-ci.org/elritsch/python-sharedmock
.. |Coverage Status| image:: https://coveralls.io/repos/github/elritsch/python-sharedmock/badge.svg?branch=master
   :target: https://coveralls.io/github/elritsch/python-sharedmock?branch=master
.. |Docs Status| image:: https://readthedocs.org/projects/python-sharedmock/badge/?version=latest
   :target: http://python-sharedmock.readthedocs.io/en/latest/?badge=latest

A multiprocessing-friendly Python mock object

Getting started
---------------

The ``SharedMock`` object has an interface similar to Python’s own
``unittest.mock.Mock``. The main difference is that the state of a
``SharedMock`` object is shared among subprocesses. This allows you to
easily test interactions of subprocesses with your mock instance.

.. code:: python

    from sharedmock.mock import SharedMock

    sharedmock = SharedMock()

    subprocess = mp.Process(target=sharedmock,
                            args=('fancyArg',))
    subprocess.start()
    subprocess.join()
    subprocess.terminate()

    expected_calls = [call('fancyArg')]
    sharedmock.assert_has_calls(expected_calls,
                                same_order=False)

If the ``SharedMock`` were to be replaced by a ``unittest.mock.Mock`` in
the example above, the assertion would fail. The interaction with the
``unittest.mock.Mock`` object would not get propagated to your test
code:

.. code:: python

    E               AssertionError: Calls not found.
    E               Expected: [call('fancyArg')]
    E               Actual: []

Source
------

The entire source code is available on `GitHub`_.

.. _GitHub: https://github.com/elritsch/python-sharedmock

Documentation
-------------

Documentation can be found on `Read the Docs`_.

.. _Read the Docs: https://python-sharedmock.readthedocs.io
