from lxml import etree


def to_xml(root, data):
    xml = etree.Element(root)

    for k, v in data.iteritems():
        child = etree.SubElement(xml, k)
        child.text = v

    return xml
