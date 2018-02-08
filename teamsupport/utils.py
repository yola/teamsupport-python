from lxml import etree
from six import iteritems


def to_xml(root, data):
    xml = etree.Element(root)

    for k, v in iteritems(data):
        child = etree.SubElement(xml, k)
        child.text = str(v) if v is not None else v

    return xml
