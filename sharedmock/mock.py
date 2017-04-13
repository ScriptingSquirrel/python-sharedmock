from multiprocessing.managers import BaseManager, BaseProxy
from unittest import mock

from sharedmock.asserters import assert_calls_equal, assert_calls_equal_unsorted


class SharedMockObj:

    def __init__(self):
        self.call_parameters = []
        self._set_return_value(None)

    def __call__(self, *args, **kwargs):
        self.call_parameters.append({'args': args, 'kwargs': kwargs})
        return self.return_value

    def _get_call_parameters(self):
        return self.call_parameters

    def _set_return_value(self, value):
        self.return_value = value

    def call_count(self):
        return len(self.call_parameters)


class SharedMockProxy(BaseProxy):
    _exposed_ = ['__call__',
                 '_get_call_parameters',
                 '_set_return_value',
                 '_set_return_value_empty_dict',
                 'assert_has_calls',
                 'call_count'
                 ]

    def __setattr__(self, name, value):
        if name == 'return_value':
            self._callmethod('_set_return_value', args=(value,))
        else:
            # forward any unknown attributes to the super class
            super().__setattr__(name, value)

    def __call__(self, *args, **kwargs):
        return self._callmethod('__call__', args, kwargs)

    def assert_has_calls(self, expected_calls, same_order):
        calls = self.mock_calls
        if same_order:
            assert_calls_equal(expected_calls, calls)
        else:
            assert_calls_equal_unsorted(expected_calls, calls)

    @property
    def call_count(self):
        return self._callmethod('call_count')

    @property
    def mock_calls(self):
        call_parameters = self._callmethod('_get_call_parameters')

        calls = []
        for cur_call in call_parameters:
            args = cur_call['args']
            kwargs = cur_call['kwargs']
            calls.append(mock.call(*args, **kwargs))
        return calls


class SharedMockManager(BaseManager):

    def __init__(self):
        BaseManager.__init__(self)


SharedMockManager.register('Mock',
                           SharedMockObj,
                           SharedMockProxy)


def SharedMock():
    """
    SharedMock factory for convenience, in order to avoid using a context manager
    to get a SharedMock object.

    NB: Consequently, this does leak the manager resource. I wonder whether there's
    a way to clean that up..?
    """
    manager = SharedMockManager()
    manager.start()
    return manager.Mock()
