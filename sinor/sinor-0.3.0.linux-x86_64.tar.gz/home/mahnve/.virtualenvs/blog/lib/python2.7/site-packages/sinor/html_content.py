import lxml.html
from lxml import etree
from sinor import file_util


EMPTY_RESULT = {'title': '',
                'date': '',
                'content': '',
                'status': '',
                'tags': []}


def _get_text_value(html, id_name):
    return _extract_data(html,
                         id_name,
                         lambda t: t.text,
                         '')


def _get_list(html, id_name):

    return _extract_data(html,
                         id_name,
                         lambda t: [li.xpath("string()") for li in t if li.xpath("string()")],
                         [])


def _get_sub_tree(html, id_name):
    return _extract_data(html,
                         id_name,
                         lambda t: etree.tostring(t),
                         '')


def _extract_data(html, id_name,  method, none_value):
    tag = html.get_element_by_id(id_name, None)
    if(tag is not None):
        return method(tag)
    else:
        return none_value


def from_file(file_name):
    return from_string(file_util.read_file(file_name),
                       {'file_name': file_name,
                        'absolute_url': file_util.absolute_href_for_file(file_name),
                        'relative_url': file_util.relative_href_for_file(file_name)})


def from_string(html_string, to_return={}):
    try:
        html = lxml.html.document_fromstring(html_string)
    except:
        return EMPTY_RESULT
    to_return['title'] = _get_text_value(html, 'post-title')
    to_return['date'] = _get_text_value(html, 'post-date')
    to_return['content'] = _get_sub_tree(html, 'post-content')
    to_return['status'] = _status(html)
    to_return['tags'] = _get_list(html, 'post-tags')
    return to_return


def _status(html):
    xpath_expression = "//*[contains(@class, 'draft')]"
    if len(html.xpath(xpath_expression)) == 0:
        return 'published'
    else:
        return 'draft'
