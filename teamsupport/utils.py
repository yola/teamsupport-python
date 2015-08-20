from lxml import etree


def to_xml(root, data=None, cdata=None):
    xml = etree.Element(root)

    if data:
        for k, v in data.iteritems():
            child = etree.SubElement(xml, k)
            child.text = v

    if cdata:
        for k, v in cdata.iteritems():
            child = etree.SubElement(xml, k)
            child.text = etree.CDATA(v)

    if not (data or cdata):
        raise TypeError(
            "to_xml() needs either a 'data' or 'cdata' argument "
            "(neither given)")

    return xml
