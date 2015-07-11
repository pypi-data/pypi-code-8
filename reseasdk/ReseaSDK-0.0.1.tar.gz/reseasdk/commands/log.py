import argparse


def log(args):
    with(open('build/{}/boot.log'.format(args.target))) as f:
         print(f.read().rstrip())


def main(args_):
    parser = argparse.ArgumentParser(prog='resea log',
                                     description='view the boot log')
    parser.add_argument('--target', default='test', help='the build target')
    args = parser.parse_args(args_)

    log(parser.parse_args(args_))
