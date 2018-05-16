# Copyright 2018 Simone Orsi
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import unittest
from werkzeug.datastructures import MultiDict
from .. import marshallers


class TestMarshallers(unittest.TestCase):

    def test_plain_values(self):
        data = MultiDict([
            ('a', '1'),
            ('b', '2'),
            ('c', '3'),
        ])
        marshalled = marshallers.marshal_request_values(data)
        self.assertEqual(marshalled['a'], '1')
        self.assertEqual(marshalled['b'], '2')
        self.assertEqual(marshalled['c'], '3')

    def test_mashal_list(self):
        data = MultiDict([
            ('a', '1'),
            ('b:list', '1'),
            ('b:list', '2'),
            ('b:list', '3'),
            ('c', '3'),
        ])
        marshalled = marshallers.marshal_request_values(data)
        self.assertEqual(marshalled['a'], '1')
        self.assertListEqual(marshalled['b'], ['1', '2', '3'])
        self.assertEqual(marshalled['c'], '3')

    def test_mashal_int(self):
        data = MultiDict([
            ('a', '1'),
            ('b:int', '2'),
            ('c:int', '3'),
            ('d:int', 'bad'),
        ])
        marshalled = marshallers.marshal_request_values(data)
        self.assertEqual(marshalled['a'], '1')
        self.assertEqual(marshalled['b'], 2)
        self.assertEqual(marshalled['c'], 3)
        self.assertEqual(marshalled['d'], 'bad')

    def test_mashal_dict(self):
        data = MultiDict([
            ('a', '1'),
            ('b.x:dict', '1'),
            ('b.y:dict', '2'),
            ('b.z:dict', '3'),
            ('c', '3'),
        ])
        marshalled = marshallers.marshal_request_values(data)
        self.assertEqual(marshalled['a'], '1')
        self.assertDictEqual(marshalled['b'], {'x': '1', 'y': '2', 'z': '3'})
        self.assertEqual(marshalled['c'], '3')
