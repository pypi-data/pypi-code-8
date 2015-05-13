import datetime, sys
from concurrent.futures import ThreadPoolExecutor

from . import download

def download_all(resolution = 5 * 60, threads = 30):
    # Download
    timestamp = int(datetime.datetime.now().timestamp())
    minute = timestamp - (timestamp % (resolution))
    with ThreadPoolExecutor(threads) as e:
        spaces = download.directory(minute).json().values()
        futures = [(space, e.submit(download.space, minute, space)) for space in spaces]
    for space, future in futures:
        if future.exception() is not None:
            sys.stderr.write('Exception downloading %s:\n%s\n\n' % (space, future.exception()))

def emit():
    import csv
    w = csv.writer(sys.stdout)
    w.writerow(('space', 'timestamp', 'open'))
    for minute in download.directory.keys():
        for space, url in download.directory[minute].json().items():
            response = download.space[minute, url]
            if response.ok:
                try:
                    data = response.json()
                except ValueError:
                    data = {}
                open = data.get('state', {}).get('open')
            else:
                open = None
            open_str = {
                True: 'TRUE',
                False: 'FALSE',
                None: 'NA',
            }[open]
            w.writerow((space, minute, open_str))

def main():
    import argparse
    p = argparse.ArgumentParser(description = 'Download Space API data.')
    p.add_argument('-d', '--download', help = 'Download new data?',
                   action = 'store_true')
    p.add_argument('-t', '--threads', default = 30, type = int,
                   help = 'Number of threads to use for downloading, default is 30')
    p.add_argument('-e', '--csv', help = 'Emit data as CSV?',
                   action = 'store_true')
    args = p.parse_args()

    if args.download:
        download_all(threads = args.threads)

    if args.csv:
        emit()

    if not args.download and not args.csv:
        sys.stderr.write('Doing nothing; try running with the --help flag.\n')
        sys.exit(1)
