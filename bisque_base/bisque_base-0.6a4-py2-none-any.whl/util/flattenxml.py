def flatten_tags(xml):
    def _xml2d(e, d, path=''):
        for child in e:
            name  = '%s%s'%(path, child.get('name', ''))
            ttype = child.get('type', None)
            value = child.get('value', None)
            if value is not None:
                if not name in d:
                    d[name] = value
                else:
                    if isinstance(d[name], list):
                        d[name].append(value)
                    else:
                        d[name] = [d[name], value]
                #if not ttype is None:
                #    d['%s.type'%name] = ttype

            d = _xml2d(child, d, path='%s%s.'%(path, child.get('name', '')))
        return d

    d = _xml2d(xml, { xml.get('name') : xml.get('value') or None }, path = xml.get('name')+'.' )
    return d


if __name__ == "__main__":
    import sys
    from lxml import etree as et
    xml="""
<tag name="xx" value="vv" >
   <tag name="yy" value="ww" />
   <tag name="yy" value="QQ" >
     <tag name="zz" value="RR" />
   </tag>
</tag>
"""
    if sys.argv < 1:
        print flatten_tags(et.XML(xml))
    else:
        print flatten_tags(et.parse(open (sys.argv[1])).getroot())
