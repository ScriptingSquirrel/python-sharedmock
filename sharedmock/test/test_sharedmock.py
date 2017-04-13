import unittest
from unittest.mock import call

import multiprocessing as mp
from sharedmock.asserters import assert_calls_equal
from sharedmock.sharedmock import SharedMock


def get_mock_return_value(result_queue, mock):
    """
    Picklable function used to test mock calls in subprocesses
    """
    return_value = mock()
    result_queue.put(return_value)


def ignore_mock(result_queue, mock):
    """
    Picklable function used to test mock calls in subprocesses
    """
    result_queue.put(None)  # to unblock caller process


def call_mock_once(result_queue, mock):
    """
    Picklable function used to test mock calls in subprocesses
    """
    mock()
    result_queue.put(None)  # to unblock caller process


def call_mock_thrice(result_queue, mock):
    """
    Picklable function used to test mock calls in subprocesses
    """
    mock()
    mock()
    mock()
    result_queue.put(None)  # to unblock caller process


def call_mock_with_args(result_queue, mock, *args, **kwargs):
    """
    Picklable function used to test mock calls in subprocesses
    """
    mock(*args, **kwargs)
    result_queue.put(None)  # to unblock caller process


class TestSharedMock(unittest.TestCase):

    def call_function_in_subprocess(self, function, args, kwargs={}):
        result_queue = mp.Queue()
        subprocess = mp.Process(target=function,
                                args=(result_queue, *args),
                                kwargs=kwargs)
        subprocess.start()
        subprocess.join()
        subprocess.terminate()

        result = result_queue.get()
        return result

    def test__instantiation__expectZeroCallCount(self):
        mock = SharedMock()

        actual_call_count = mock.call_count
        expected_call_count = 0
        self.assertEqual(expected_call_count, actual_call_count)

    def test__instantiation__expectNoneReturnValue(self):
        mock = SharedMock()

        actual_return_value = mock()
        expected_return_value = None
        self.assertEqual(expected_return_value, actual_return_value)

    def test__instantiation__expectEmptyMockCalls(self):
        mock = SharedMock()

        actual_mock_calls = mock.mock_calls
        expected_mock_calls = []
        self.assertEqual(expected_mock_calls, actual_mock_calls)

    def test__unsetReturnValue__expectNoneValueReturnedInsideSubprocess(self):
        mock = SharedMock()
        actual_return_value = self.call_function_in_subprocess(function=get_mock_return_value,
                                                               args=(mock,))
        expected_return_value = None
        self.assertEqual(expected_return_value, actual_return_value)

    def test__customReturnValue__expectCustomValueReturnedInsideSubprocess(self):
        mock = SharedMock()
        mock.return_value = (
            'this', 444, 'is', ('some',), 9, ['complex', 'stuff']
        )

        actual_return_value = self.call_function_in_subprocess(function=get_mock_return_value,
                                                               args=(mock,))
        expected_return_value = (
            'this', 444, 'is', ('some',), 9, ['complex', 'stuff']
        )
        self.assertEqual(expected_return_value, actual_return_value)

    def test__emptyDictReturnValue__expectEmptyDictValueReturnedInsideSubprocess(self):
        mock = SharedMock()
        mock.return_value = {}

        actual_return_value = self.call_function_in_subprocess(function=get_mock_return_value,
                                                               args=(mock,))
        expected_return_value = {}
        self.assertEqual(expected_return_value, actual_return_value)

    def test__mockIgnoredInSubprocesses__expectZeroCallCount(self):
        mock = SharedMock()
        self.call_function_in_subprocess(function=ignore_mock,
                                         args=(mock,))
        self.call_function_in_subprocess(function=ignore_mock,
                                         args=(mock,))

        actual_call_count = mock.call_count
        expected_call_count = 0
        self.assertEqual(expected_call_count, actual_call_count)

    def test__multipleMockCallsInMultipleSubprocesses__expectCorrectOverallMockCallCount(self):
        mock = SharedMock()
        self.call_function_in_subprocess(function=call_mock_once,
                                         args=(mock,))
        self.call_function_in_subprocess(function=call_mock_thrice,
                                         args=(mock,))
        self.call_function_in_subprocess(function=call_mock_once,
                                         args=(mock,))
        self.call_function_in_subprocess(function=call_mock_thrice,
                                         args=(mock,))

        actual_call_count = mock.call_count
        expected_call_count = 1 + 3 + 1 + 3
        self.assertEqual(expected_call_count, actual_call_count)

    def test__multipleMockCallsWithDifferentArgumentsInMultipleSubprocesses__expectAllMockCallsPresent(self):
        mock = SharedMock()
        # args and kwargs
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 1, 2, 3),
                                         kwargs={'a': 345, 'another': 'xxx'})
        # only one arg
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 12345))
        # no args
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock,))

        actual_calls = mock.mock_calls
        expected_calls = [call(1, 2, 3, a=345, another='xxx'),
                          call(12345),
                          call()]
        assert_calls_equal(expected_calls, actual_calls)

    def test__assert_has_calls__orderedIdenticalCalls__expectSuccess(self):
        mock = SharedMock()
        # args and kwargs
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 1, 2, 3),
                                         kwargs={'a': 345, 'another': 'xxx'})
        # only one arg
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 12345))
        # no args
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock,))

        expected_calls = [call(1, 2, 3, a=345, another='xxx'),
                          call(12345),
                          call()]
        mock.assert_has_calls(expected_calls, same_order=True)

    def test__assert_has_calls__orderedIdenticalCallsAnyOrderAccepted__expectSuccess(self):
        mock = SharedMock()
        # args and kwargs
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 1, 2, 3),
                                         kwargs={'a': 345, 'another': 'xxx'})
        # only one arg
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 12345))
        # no args
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock,))

        expected_calls = [call(1, 2, 3, a=345, another='xxx'),
                          call(12345),
                          call()]
        mock.assert_has_calls(expected_calls, same_order=False)

    def test__assert_has_calls__orderedNonIdenticalCalls__expectAssertionError(self):
        mock = SharedMock()
        # args and kwargs
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 1, 2, 3),
                                         kwargs={'a': 345, 'another': 'xxx'})
        # only one arg
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 12345))
        # no args
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock,))

        expected_calls = [call(1, 2, 3, a=345, another='xxx'),
                          call(123456),  # different! was called: call(12345)
                          call()]
        with self.assertRaises(AssertionError):
            mock.assert_has_calls(expected_calls, same_order=True)

    def test__assert_has_calls__unorderedIdenticalCalls__expectAssertionError(self):
        mock = SharedMock()
        # args and kwargs
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 1, 2, 3),
                                         kwargs={'a': 345, 'another': 'xxx'})
        # only one arg
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 12345))
        # no args
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock,))

        expected_calls = [call(12345),
                          call(),
                          call(1, 2, 3, a=345, another='xxx'),
                          ]
        with self.assertRaises(AssertionError):
            mock.assert_has_calls(expected_calls, same_order=True)

    def test__assert_has_calls__unorderedIdenticalCallsAnyOrderAccepted__expectSuccess(self):
        mock = SharedMock()
        # args and kwargs
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 1, 2, 3),
                                         kwargs={'a': 345, 'another': 'xxx'})
        # only one arg
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 12345))
        # no args
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock,))

        expected_calls = [call(12345),
                          call(),
                          call(1, 2, 3, a=345, another='xxx'),
                          ]
        mock.assert_has_calls(expected_calls, same_order=False)

    def test__assert_has_calls__unorderedNonIdenticalCallsAnyOrderAccepted__expectAssertionError(self):
        mock = SharedMock()
        # args and kwargs
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 1, 2, 3),
                                         kwargs={'a': 345, 'another': 'xxx'})
        # only one arg
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock, 12345))
        # no args
        self.call_function_in_subprocess(function=call_mock_with_args,
                                         args=(mock,))

        expected_calls = [call(12345),
                          call(1),  # different! was called: call()
                          call(1, 2, 3, a=345, another='xxx'),
                          ]
        with self.assertRaises(AssertionError):
            mock.assert_has_calls(expected_calls, same_order=False)

    def test__assert_has_calls__noCalls__expectSuccessWithSameOrderTrue(self):
        mock = SharedMock()
        self.call_function_in_subprocess(function=ignore_mock,
                                         args=(mock,))
        self.call_function_in_subprocess(function=ignore_mock,
                                         args=(mock,))

        expected_calls = []
        mock.assert_has_calls(expected_calls, same_order=True)

    def test__assert_has_calls__noCalls__expectSuccessWithSameOrderFalse(self):
        mock = SharedMock()
        self.call_function_in_subprocess(function=ignore_mock,
                                         args=(mock,))
        self.call_function_in_subprocess(function=ignore_mock,
                                         args=(mock,))

        expected_calls = []
        mock.assert_has_calls(expected_calls, same_order=False)
