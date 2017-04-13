import unittest
from unittest.mock import call

from asserters import assert_calls_equal


class Test_assert_calls_equal(unittest.TestCase):

    def test_equal_lists_empty(self):
        expected = []
        test = []
        assert_calls_equal(expected, test)

    def test_equal_same_list(self):
        data = [call.afunction('was', 'called', too=2)]
        assert_calls_equal(data, data)

    def test_equal_list_one_item(self):
        expected = [call.a("something")]
        test = [call.a("something")]
        assert_calls_equal(expected, test)

    def test_equal_list_multiple_items(self):
        expected = [call.a("something"),
                    call.long_function('with', a="paramter", se=4),
                    call.other_function(),
                    call.one_more(99.3)]
        assert_calls_equal(expected, expected)

    def test_equal_single_call(self):
        expected = call.a("something")
        assert_calls_equal(expected, expected)

    def test_not_equal_single_call(self):
        expected = call.a("something")
        test = call.a("something_else")
        self.assertRaisesRegex(AssertionError, "\nExpected calls:\n"
                                               "call\.a\('something'\)\n"
                                               "Actual calls:\n"
                                               "call\.a\('something_else'\)",
                               assert_calls_equal, expected, test)

    def test_not_equal_lists_one_item(self):
        expected = [call.a("something")]
        test = [call.a("something_else")]
        self.assertRaisesRegex(AssertionError, "\nExpected calls:\n"
                                               "\[call\.a\('something'\)\]\n"
                                               "Actual calls:\n"
                                               "\[call\.a\('something_else'\)\]",
                               assert_calls_equal, expected, test)

    def test_not_equal_lists_different_num_items(self):
        expected = [call.a("something")]
        test = [call.a("something"),
                call.a("something")]
        self.assertRaisesRegex(AssertionError, "\nExpected calls:\n"
                                               "\[call\.a\('something'\)\]\n"
                                               "Actual calls:\n"
                                               "\[call\.a\('something'\), call\.a\('something'\)\]",
                               assert_calls_equal, expected, test)

    def test_not_equal_lists_with_same_num_items(self):
        expected = [call.a("something"),
                    call.a("something", 99, f=3.99)]
        test = [call.a("something"),
                call.a("something")]
        self.assertRaisesRegex(AssertionError, "\nExpected calls:\n"
                                               "\[call\.a\('something'\), call\.a\('something', 99, f=3.99\)\]\n"
                                               "Actual calls:\n"
                                               "\[call\.a\('something'\), call\.a\('something'\)\]",
                               assert_calls_equal, expected, test)

    def test_not_equal_lists_with_invers_ordering(self):
        expected = [call.a("something", 'here'),
                    call.func("something", 99, f=3.99)]
        test = [call.func("something", 99, f=3.99),
                call.a("something", 'here')]
        self.assertRaisesRegex(AssertionError, "\nExpected calls:\n"
                                               "\[call\.a\('something', 'here'\), call\.func\('something', 99, f=3\.99\)\]\n"
                                               "Actual calls:\n"
                                               "\[call\.func\('something', 99, f=3\.99\), call\.a\('something', 'here'\)\]",
                               assert_calls_equal, expected, test)

    def test_not_equal_lists_one_empty(self):
        expected = [call.a("something", 'here'),
                    call.func("something", 99, f=3.99)]
        test = []
        self.assertRaisesRegex(AssertionError, "\nExpected calls:\n"
                                               "\[call\.a\('something', 'here'\), call\.func\('something', 99, f=3\.99\)\]\n"
                                               "Actual calls:\n"
                                               "\[\]",
                               assert_calls_equal, expected, test)
