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

Yeilds:

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

# Constructor Options

## xml_declaration

Output the XML declaration. Defaults to `False`.

    p2x = PyToXml("doc", "hello", encoding="latin1", xml_declaration=True)
    print p2x.encode()

Yields:

    <?xml version='1.0' encoding='latin1'?>
    <doc>hello</doc>

## encoding

Which encoding system should be used to build Defaults to `UTF-8`.
