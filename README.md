[![Build Status](https://secure.travis-ci.org/skimhub/pyToXml.png?branch=master)](http://travis-ci.org/skimhub/pyToXml)

# Synopsis

    from pytoxml import PyToXml

    person_details = {
        "name": "Bob",
        "occupation": "Builder",
        "arrests": [
            "Assault / Battery",
            "Indecent Exposure"
        ]
    }

    p2x = PyToXml("doc", person_details)
    print p2x.encode()

Yields:

    <doc>
      <arrests>
        <item>Assault / Battery</item>
        <item>Indecent Exposure</item>
      </arrests>
      <name>Bob</name>
      <occupation>Builder</occupation>
    </doc>

# Introduction

pytoxml gives you a simple way of converting a python structure to
XML.

# Tests

Run the test suite with `py.test` (`pip install pytest`) from the root
of the project.

# Pluralisation of lists

By default pytoxml will use the element name `item` which is probably
not what you want. Here's a simple example of how you might use a map
to determine the best phrase for a list element:

    class BetterListsDemo(PyToXml):
        def pluralisation(self, plural):
            pluralisation_map = {
                "arrests": "arrest"
            }

            return pluralisation_map.get(plural) or "item"

    p2x = BetterListsDemo("doc", person_details)
    print p2x.encode()

Which gives:

    <doc>
      <arrests>
        <arrest>Assault / Battery</arrest>
        <arrest>Indecent Exposure</arrest>
      </arrests>
      <name>Bob</name>
      <occupation>Builder</occupation>
    </doc>

The `pluralisation` function takes `plural` as an argument which is
the name of the direct parent element to the one you'll be creating.

# Custom Handlers

By default pytoxml will only encode a few types, if you want to
encode, for example, exceptions, you might do the following:

    def temp_convertor(structure, element, name):
        element.text = str(structure)

    p2x = PyToXml("a", { "b": Exception("Should now serialise") })
    p2x.add_type_handler(Exception, temp_convertor)
    self.assertEqual(str(p2x.encode()), "<a><b>Should now serialise</b></a>")

If you give an object a `__pytoxml__` method then you don't need to
register a handler:

    class MyException(Exception):
        def __pytoxml__(self, structure, element, name):
            element.text = str(self)

        p2x = PyToXml("a", { "b": MyException("Should now serialise") })
        self.assertEqual(str(p2x.encode()), "<a><b>Should now serialise</b></a>")

# CData and attributes

Though it's somewhat orthogonal to the original justification of
PyToXml, you can easily output CDATA elements and attributes:

    from pytoxml import PyToXml

    cdata = pytoxml.CData("<crappy>xml")
    attributes = pytoxml.Attributes("simple text", {"one": "two"})

    p2x = pytoxml.PyToXml("root", { "raw": cdata, "attributed": attributes })
    p2x.encode()

gives (un-formatted):

    <?xml version="1.0"?>
    <root>
      <raw><![CDATA[<crappy>xml]]></raw>
      <attributed one="two">simple text</attributed>
    </root>

# Constructor Options

## xml_declaration

Output the XML declaration. Defaults to `False`.

    p2x = PyToXml("doc", "hello", encoding="latin1", xml_declaration=True)
    print p2x.encode()

Yields:

    <?xml version='1.0' encoding='latin1'?>
    <doc>hello</doc>

## encoding

# Attributes on the root element

    p2x = PyToXml("a", { }, root_attributes={"one": "two"} )
    p2x.encode()

gives:

    <a one="two"/>

Which encoding system should be used to build Defaults to `UTF-8`.

# Licence

Copyright (C) 2012-2014 Skimbit LTD.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
