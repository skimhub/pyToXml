from types import (DictType, StringTypes, IntType, FloatType, LongType,
                   TupleType, ListType, BooleanType)

from lxml import etree


class Attributes(object):
    def __init__(self, data, attributes):
        self.data       = data
        self.attributes = attributes

    def __pytoxml__(self, structure, element, name, pytoxml):

        for key, value in self.attributes.items():
            element.set(key, value)

        if self.data:
            if isinstance(self.data, DictType):
                pytoxml.type_builder_dict(self.data, element, name, pytoxml)
            else:
                element.text = self.data


class CData(object):
    def __init__(self, string):
        self.string = string

    def __pytoxml__(self, structure, element, name, pytoxml):
        element.text = etree.CDATA(unicode(self.string))


class PyToXml(object):
    """Class which allows you convert a deeply nested python structure
    into an XML representation."""
    def __init__(self, root_name, structure,
                 encoding="UTF-8", xml_declaration=False, root_attributes={}):
        self.root = etree.Element(root_name, root_attributes)
        self.root_name = root_name
        self.structure = structure
        self.encoding = encoding
        self.xml_declaration = xml_declaration

        self._flat_type_map = self.build_flat_type_map(self.type_map())

    def build_flat_type_map(self, type_func_map):
        """Flatten the types so we can access them as quickly as
        possible."""
        type_list = {}

        for typ, outputter in type_func_map.items():
            # there might be tuples thanks to things like StringTypes
            if isinstance(typ, TupleType):
                for subtype in typ:
                    type_list[subtype] = outputter
            else:
                type_list[typ] = outputter

        return type_list

    def pluralisation(self, plural):
        """Returns a string that is suitable for elements of a
        list. Intended to be overridden for more complex pluralisation
        logic."""
        return "item"

    def type_builder_list(self, structure, element, name, pytoxml):
        for value in structure:
            sub = etree.SubElement(element, self.pluralisation(name))
            self.traverse(value, sub, name)

    def type_builder_string(self, structure, element, name, pytoxml):
        element.text = structure

    def type_builder_dict(self, structure, element, name, pytoxml):
        for key, value in structure.iteritems():
            sub = etree.SubElement(element, key)
            self.traverse(value, sub, key)

    def type_builder_number(self, structure, element, name, pytoxml):
        element.text = str(structure)

    def type_builder_bool(self, structure, element, name, pytoxml):
        element.text = str(structure).lower()

    def add_type_handler(self, typ, handler=None):
        new_map = { }
        new_map[typ] = handler

        self._flat_type_map = dict(self._flat_type_map.items()
                                   + self.build_flat_type_map(new_map).items())

    def type_map(self):
        return {
            # lists
            ListType: self.type_builder_list,
            TupleType: self.type_builder_list,

            # numerical
            IntType: self.type_builder_number,
            FloatType: self.type_builder_number,
            LongType: self.type_builder_number,

            # other
            StringTypes: self.type_builder_string,
            DictType: self.type_builder_dict,
            BooleanType: self.type_builder_bool
        }

    def traverse(self, structure, element, name):
        """Loop over the structure, convert to an etree style element
        and apply to element. The argument `name` is the element name
        of the parent."""
        typ = type(structure)
        processor = self._flat_type_map.get(typ)

        if not processor:
            # if we find a __pytoxml__ then use that
            if hasattr(structure, "__pytoxml__"):
                processor = structure.__pytoxml__
            else:
                raise TypeError("Don't know how to serialise %s." % typ)

        return processor(structure, element, name, self)

    def encode(self):
        """Encode the structure passed into the constructor as
        XML. This method must be called before this object is output
        as a string."""
        self.traverse(self.structure, self.root, self.root_name)

        return self

    def __str__(self):
        """Output the XML."""
        return etree.tostring(self.root,
                              encoding=self.encoding,
                              xml_declaration=self.xml_declaration)
