#!/usr/bin/python


import os
import re
import argparse


SRC_JS_REGEX = '([^\s\*]*\.js)+'
SRC_DOC_REGEX = '(\/\*\*(.*\n\s*\*.*@src)(?:(?!\*\/).|[\n\r])*\*\/)'


def get_src_doc(template):
    """get_src_doc

    Returns documented sources

    Args:
        template (str): Template source
    Returns:
        str: JsDoc with @src tag
    """
    matches = re.findall(SRC_DOC_REGEX, template)
    src_docs = []
    for match in matches:
        if match and len(match) > 0:
            src_docs.append(match[0])
    return '\n'.join(src_docs)


def get_source_paths(src_doc):
    """get_source_paths

    Returns sources list stored in src_doc

    Args:
        src_doc (str): JsDoc with @src tag
    Returns:
        list: List of sources
    """
    sources = []
    matches = re.findall(SRC_JS_REGEX, src_doc)
    if matches:
        for match in matches:
            if match:
                sources.append(match)
    return sources


def render(template_path):
    """render

    Renders template with sources documented in it

    Args:
        template_path (str): Path to template
    Returns:
        str: Rendered template
    """
    with open(template_path, 'r') as template_file:
        template = template_file.read()
    src_doc = get_src_doc(template)
    source_paths = get_source_paths(src_doc)
    code = ''
    for source_path in source_paths:
        with open(source_path, 'r') as source_file:
            code += source_file.read()
    return template.replace(src_doc, code)


def create_output(output_path, src):
    """create_output

    Creates result file with given source

    Args:
        output_path (str): Path to new file
        src (str): File data
    Returns:
        None
    """
    dir_path = os.path.dirname(output_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(output_path, 'a') as file:
        file.write(src)


def build(template_path, output_dir):
    """build

    Builds js file from template with sources

    Args:
        template_path (str): Path to template
        output_dir (str): Path to output directory
    Returns:
        None
    """
    src = render(template_path)
    output_path = os.path.join(output_dir, os.path.basename(template_path))
    create_output(output_path, src)


def main():
    parser = argparse.ArgumentParser(
        description='Build js files from templates with sources')
    parser.add_argument('templates',
                        metavar='T',
                        type=str,
                        nargs='+',
                        help='path to template')
    parser.add_argument('-o', '--out',
                        dest='output',
                        action='store',
                        default='bin',
                        help='path to output directory')

    args = parser.parse_args()

    for template_path in args.templates:
        if os.path.exists(template_path):
            build(template_path, args.output)


if __name__ == "__main__":
    main()
