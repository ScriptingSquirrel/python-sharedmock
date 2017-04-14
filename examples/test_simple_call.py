import unittest

from unittest.mock import call
from sharedmock.mock import SharedMock
import multiprocessing as mp


class TestMySubprocesses(unittest.TestCase):

    def test_call(self):
        sharedmock = SharedMock()

        subprocess = mp.Process(target=sharedmock,
                                args=('fancyArg',))
        subprocess.start()
        subprocess.join()
        subprocess.terminate()

        expected_calls = [call('fancyArg')]
        sharedmock.assert_has_calls(expected_calls,
                                    same_order=False)
