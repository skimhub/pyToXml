from lxml import etree

class PyToXml(object):
    def __init__(self, root_element_name, structure):
        self.root = etree.Element(root_element_name)
        self.structure = structure

    def traverse(self, structure, document):
 
        if isinstance(structure, dict):
            for key, value in structure.iteritems():
                etree.SubElement(document, key)

    def to_xml(self):
        return self.traverse(self.structure, self.root)

    def __str__(self):
        return etree.tostring(self.root, pretty_print=True)

if __name__ == "__main__":
    s = {
        "hello": 1,
        "world": 2
    }

    p2x = PyToXml("root", s)
    p2x.to_xml()
    print p2x
