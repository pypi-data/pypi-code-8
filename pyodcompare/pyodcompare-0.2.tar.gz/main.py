import argparse
import os
from pyodcompare import DocumentCompare
import sys

def execute():

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('changed_file', metavar='mydoc_v2.doc',type=str,
                       help='Changed file')
    parser.add_argument('original_file', metavar='mydoc_v1.doc', type=str,
                       help='Original file')
    parser.add_argument('target_file', metavar='mydoc_diff.odt', type=str,
                       help='Target diff file (an ODT file)')
    parser.add_argument('--host', dest='host', type=str,
                       default='localhost',
                       help='LibreOffice service host')
    parser.add_argument('--port', dest='port', type=int,
                       default=2002,
                       help='LibreOffice service port')

    parsed = parser.parse_args()

    try:
        compare = DocumentCompare(listener=(parsed.host, parsed.port))
        compare.compare(os.path.abspath(parsed.changed_file),
                        os.path.abspath(parsed.original_file),
                        os.path.abspath(parsed.target_file),
                        )
    except Exception as error:
        sys.stderr.write(str(error) + "\n")
        sys.exit(1)
