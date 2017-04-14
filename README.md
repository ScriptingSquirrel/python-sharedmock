[![Build Status](https://travis-ci.org/elritsch/python-sharedmock.svg?branch=master)](https://travis-ci.org/elritsch/python-sharedmock)
[![Coverage Status](https://coveralls.io/repos/github/elritsch/python-sharedmock/badge.svg?branch=master)](https://coveralls.io/github/elritsch/python-sharedmock?branch=master)

# python-sharedmock
A multiprocessing-friendly Python mock object

## Getting started

The `SharedMock` object has an interface similar to Python's own `unittest.mock.Mock`. The main difference is that the state of a `SharedMock` object is shared among subprocesses. This allows you to easily test interactions of subprocesses with your mock instance.

```python
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
```

If the `SharedMock` were to be replaced by a `unittest.mock.Mock` in the example above, the assertion would fail. The interaction with the `unittest.mock.Mock` object would not get propagated to your test code:
```python
E               AssertionError: Calls not found.
E               Expected: [call('fancyArg')]
E               Actual: []
```
