from lxml import etree
from six import iteritems, text_type


def to_xml(root, data):
    xml = etree.Element(root)

    for k, v in iteritems(data):
        child = etree.SubElement(xml, k)
        child.text = text_type(v) if v is not None else ''

    return xml
