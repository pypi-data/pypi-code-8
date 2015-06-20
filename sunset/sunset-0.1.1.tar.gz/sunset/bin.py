import sys
import logging
import argparse
import sunset.tool


def scan(args):
    scanner = sunset.tool.ScanTool.config_from_args(args)
    scanner.start_scan()
    sys.exit(scanner.scanlog.get_message_count('ALERT'))


def main():
    parser = argparse.ArgumentParser(prog='sunset')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')

    subparsers = parser.add_subparsers(help='sub-command help')

    # "scan" command
    scan_parser = subparsers.add_parser('scan', help='Scans for expiring/expired code.')
    scan_parser.add_argument('-R', '--recursive', action='store_true', help='Scan recursively')
    scan_parser.add_argument('-w', '--within', type=str, help='Days from today to limit alerts/warnings (e.g. "5d" for 5 days)')
    scan_parser.add_argument('-l', '--levels', type=str, help='Only show messages of this level (e.g. "ALERT", "WARNING").')
    scan_parser.add_argument('-o', '--output', type=str, choices=('CSV',), help='Output to different format (CSV only for now)')
    scan_parser.add_argument('files', type=str, nargs='+', help='Files to scan')
    scan_parser.set_defaults(func=scan)

    args = parser.parse_args()

    if args.debug:
        logger = logging.getLogger('sunset')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.StreamHandler(sys.stderr))

    args.func(args)
