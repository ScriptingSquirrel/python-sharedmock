from pprint import pformat


def assert_calls_equal(expected, actual):
    """
    Check whether the given mock object (or mock method) calls are equal and
    return a nicely formatted message.
    """
    if not expected == actual:
        raise_calls_differ_error(expected, actual)


def raise_calls_differ_error(expected, actual):
    """
    Raise an AssertionError with pretty print format for the given expected
    and actual mock calls in order to ensure consistent print style for better
    readability.
    """
    expected_str = pformat(expected)
    actual_str = pformat(actual)
    msg = '\nMock calls differ!\nExpected calls:\n{}\nActual calls:\n{}'.format(
        expected_str,
        actual_str
    )
    raise AssertionError(msg)


def assert_calls_equal_unsorted(expected, actual):
    """
    Raises an AssertionError if the two iterables do not contain the same items.

    The order of the items is ignored
    """
    for expected in expected:
        if expected not in actual:
            raise_calls_differ_error(expected, actual)
