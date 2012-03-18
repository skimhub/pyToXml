import unittest
from lxml import etree

class PyToXml(object):
    def __init__(self, root_element_name, structure):
        self.root = etree.Element(root_element_name)
        self.structure = structure

    def traverse(self, structure, document):
        if type(structure) == str:
            document.text = structure

        if type(structure) in [ int, float ]:
            document.text = str(structure)

        if type(structure) == dict:
            for key, value in structure.iteritems():
                sub = etree.SubElement(document, key)
                self.traverse(value, sub)

    def to_xml(self):
        return self.traverse(self.structure, self.root)

    def __str__(self):
        return etree.tostring(self.root)


class TestPyToXml(unittest.TestCase):
    def test_simple_root(self):
        p2x = PyToXml("a_root_element", {})
        self.assertEqual(str(p2x), "<a_root_element/>")

    def test_invalid_root_element(self):
        """No XML chars allowed in the element names. """
        self.assertRaises(ValueError, PyToXml, "a<root>element", {})

    def test_int_values(self):
        p2x = PyToXml("root", { "one": 2 })
        p2x.to_xml()
        self.assertEqual(str(p2x), "<root><one>2</one></root>")

    def test_float_values(self):
        p2x = PyToXml("root", { "one": 2.3 })
        p2x.to_xml()
        self.assertEqual(str(p2x), "<root><one>2.3</one></root>")

    def test_string_values(self):
        p2x = PyToXml("root", { "one": "two" })
        p2x.to_xml()
        self.assertEqual(str(p2x), "<root><one>two</one></root>")

    def test_embedded_dict_values(self):
        p2x = PyToXml("root", { "a": { "b": "c" } })
        p2x.to_xml()
        self.assertEqual(str(p2x), "<root><a><b>c</b></a></root>")

if __name__ == '__main__':
    unittest.main()
