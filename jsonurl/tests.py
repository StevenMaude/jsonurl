from __future__ import (absolute_import, division,
                        print_function, unicode_literals) 

import unittest
import jsonurl

# Functional tests, taken from jsonurl README.
class TestFlatDictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = {"one": 1, "two": 2}
        cls.query_string = jsonurl.query_string(d)

    def test_flat_dictionary_to_query_string(self):
        self.assertEqual('one=1&two=2', self.query_string)


class TestNestedDictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = {"one": {"two": 2, "three": 3}, "four": 4}
        cls.query_string = jsonurl.query_string(cls.d)
        cls.args = jsonurl.dict_to_args(cls.d)
        cls.parsed_query = jsonurl.parse_query(cls.query_string)

    def test_nested_dictionary_to_query_string(self):
        self.assertEqual('four=4&one.three=3&one.two=2', self.query_string)

    def test_nested_dictionary_to_args(self):
        self.assertEqual({'four': '4', 'one.three': '3', 'one.two': '2'},
                     self.args)

    def test_parse_nested_dictionary_query(self):
        self.assertEqual(self.d, self.parsed_query)


class TestNestedList(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = {"one": 1, "two": [2, 3, 4]}
        cls.query_string = jsonurl.query_string(cls.d)
        cls.args = jsonurl.dict_to_args(cls.d)
        cls.parsed_query = jsonurl.parse_query(cls.query_string)

    def test_nested_list_to_query_string(self):
        self.assertEqual('one=1&two.0=2&two.1=3&two.2=4', self.query_string)

    def test_nested_list_to_args(self):
        self.assertEqual({'two.1': '3', 'two.0': '2', 'two.2': '4', 'one': '1'},
                     self.args)
    
    def test_parse_nested_list_query(self):
        self.assertEqual(self.d, self.parsed_query)


class TestListInDictionary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = {"one" : [ {"two" : 2, "three" : 3}, 4 ]}
        cls.query_string = jsonurl.query_string(d)

    def test_list_in_dictionary_to_query_string(self):
        self.assertEqual('one.0.three=3&one.0.two=2&one.1=4', self.query_string)


class TestUrlEscaping(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = {"escape_me" : "I'll need escaping"}
        cls.query_string = jsonurl.query_string(cls.d)
        cls.parsed_query = jsonurl.parse_query(cls.query_string)

    def test_query_string_escaping(self):
        self.assertEqual('escape_me=I%27ll+need+escaping', self.query_string)

    def test_parse_escaped_query_string(self):
        self.assertEqual(self.d, self.parsed_query)


class TestDotEscaping(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = {"user.names" : ["richard", "jones"]}
        cls.query_string = jsonurl.query_string(cls.d)
        cls.parsed_query = jsonurl.parse_query(cls.query_string)

    def test_dot_escaping(self):
        self.assertEqual(self.d, self.parsed_query)


class TestParameterOrdering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        d = {"b": "last", "a": [1, 2, 3]}
        cls.query_string = jsonurl.query_string(d)

    def test_parameter_ordering(self):
        self.assertEqual('a.0=1&a.1=2&a.2=3&b=last', self.query_string)
