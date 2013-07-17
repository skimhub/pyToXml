# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
try:
    import unittest2 as unittest
except:
    import unittest

import six
import pytest

from pytoxml import PyToXml, Attributes, CData


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

    def test_six_integer_types(self):
        for six_type in six.integer_types:
            p2x = PyToXml("root", { "one": six_type(2) })
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

    def test_tuple_values(self):
        p2x = PyToXml("root", { "a": (1, 2) })
        p2x.encode()

        output = "<root><a><item>1</item><item>2</item></a></root>"
        self.assertEqual(str(p2x), output)

    def test_unicode(self):
        p2x = PyToXml("root", { "a": u"\u2603" })
        p2x.encode()

        output = u"<root><a>☃</a></root>"
        self.assertEqual(six.text_type(p2x), output)

    def test_xmldecloration_default_encoding(self):
        p2x = PyToXml("root", "hi", xml_declaration=True)
        self.assertEqual(str(p2x.encode()),
                         "<?xml version='1.0' encoding='UTF-8'?>\n<root>hi</root>")

    def test_xmldecloration_custom_encoding(self):
        p2x = PyToXml("root", "hi", xml_declaration=True, encoding="latin1")
        self.assertEqual(str(p2x.encode()),
                         "<?xml version='1.0' encoding='latin1'?>\n<root>hi</root>")

    def test_booleans(self):
        p2x = PyToXml("root", { "bald": True })
        self.assertEqual(str(p2x.encode()), "<root><bald>true</bald></root>")

    def test_type_unknown(self):
        p2x = PyToXml("root", { "unknown": Exception("Shouldn't serialise") })
        self.assertRaises(TypeError, p2x.encode)

    def test_add_type_handler(self):
        def temp_convertor(structure, element, name, pytoxml):
            element.text = str(structure)

        p2x = PyToXml("a", { "b": Exception("Should now serialise") })
        p2x.add_type_handler(Exception, temp_convertor)

        self.assertEqual(str(p2x.encode()), "<a><b>Should now serialise</b></a>")

    def test_cdata(self):
        cdata = CData("<xml>is pretty</horrible>")

        p2x = PyToXml("a", { "b": cdata } )
        self.assertEqual(str(p2x.encode()),
                         "<a><b><![CDATA[<xml>is pretty</horrible>]]></b></a>")

    def test_attributes_with_text(self):
        attrs = Attributes("c", { "one": "two" })

        p2x = PyToXml("a", { "b": attrs } )
        self.assertEqual(str(p2x.encode()),
                         "<a><b one=\"two\">c</b></a>")

    def test_attributes_with_dict(self):
        attrs = Attributes({'test': 'name'}, { "one": "two" })

        p2x = PyToXml("a", { "b": attrs } )
        self.assertEqual(str(p2x.encode()),
                         "<a><b one=\"two\"><test>name</test></b></a>")

    def test_attributes_without_text(self):
        attrs = Attributes(None, { "one": "two" })

        p2x = PyToXml("a", { "b": attrs } )
        p2x.add_type_handler(Attributes)

        self.assertEqual(str(p2x.encode()), "<a><b one=\"two\"/></a>")

    def test_attributes_on_root(self):
        p2x = PyToXml("a", { }, root_attributes={"one": "two"} )
        self.assertEqual(str(p2x.encode()), "<a one=\"two\"/>")

    def test_illegal_unicode(self):
        "Illegal unicode errors unless told to escape"
        p2x = PyToXml("root", {"a": u"\u001a"})
        with pytest.raises(ValueError):
            p2x.encode()

        p2x = PyToXml("root", {"a": u"\u001a"}, escape_illegal_chars=True)
        text = p2x.encode()
        assert str(text) == "<root><a></a></root>"


if __name__ == '__main__':
    unittest.main()
