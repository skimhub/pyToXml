# -*- coding: utf-8 -*-

import unittest
from lxml import etree

class PyToXml(object):
    def __init__(self, root_name, structure, encoding="UTF-8", xml_declaration=False):
        self.root = etree.Element(root_name)
        self.root_name = root_name
        self.structure = structure
        self.encoding = encoding
        self.xml_declaration = xml_declaration
    
    def pluralisation(self, plural):
        return "item"

    def traverse(self, structure, document, name):
        if type(structure) in [ basestring, str, unicode ]:
            document.text = structure

        if type(structure) in [ int, float ]:
            document.text = str(structure)

        if type(structure) == list:
            for value in structure:
                sub = etree.SubElement(document, self.pluralisation(name))
                self.traverse(value, sub, name)

        if type(structure) == dict:
            for key, value in structure.iteritems():
                sub = etree.SubElement(document, key)
                self.traverse(value, sub, key)

    def encode(self):
        return self.traverse(self.structure, self.root, self.root_name)

    def __str__(self):
        return etree.tostring(self.root,
                              encoding=self.encoding,
                              xml_declaration=self.xml_declaration)


class TestPyToXml(unittest.TestCase):
    def test_simple_root(self):
        p2x = PyToXml("a_root_element", {})
        self.assertEqual(str(p2x), "<a_root_element/>")

    def test_invalid_root_element(self):
        """No XML chars allowed in the element names. """
        self.assertRaises(ValueError, PyToXml, "a<root>element", {})

    def test_int_values(self):
        p2x = PyToXml("root", { "one": 2 })
        p2x.encode()
        self.assertEqual(str(p2x), "<root><one>2</one></root>")

    def test_float_values(self):
        p2x = PyToXml("root", { "one": 2.3 })
        p2x.encode()
        self.assertEqual(str(p2x), "<root><one>2.3</one></root>")

    def test_string_values(self):
        p2x = PyToXml("root", { "one": "two" })
        p2x.encode()
        self.assertEqual(str(p2x), "<root><one>two</one></root>")

    def test_embedded_dict_values(self):
        p2x = PyToXml("root", { "a": { "b": "c" } })
        p2x.encode()
        self.assertEqual(str(p2x), "<root><a><b>c</b></a></root>")

    def test_list_values(self):
        p2x = PyToXml("root", { "a": [1, 2] })
        p2x.encode()

        output = "<root><a><item>1</item><item>2</item></a></root>"
        self.assertEqual(str(p2x), output)

    def test_unicode(self):
        p2x = PyToXml("root", { "a": u"\u2603" })
        p2x.encode()

        output = "<root><a>☃</a></root>"
        self.assertEqual(str(p2x), output)

if __name__ == '__main__':
    unittest.main()
