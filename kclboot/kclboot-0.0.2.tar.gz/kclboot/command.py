import argparse
import sys
from kclboot import Bootstrapper

def _download(args):
    b = Bootstrapper(args.jar_folder)
    print(b.download_jars())

def _command(args):
    b = Bootstrapper(args.jar_folder, args.properties_file)
    print(b.command)

def _classpath(args):
    b = Bootstrapper(args.jar_folder, args.properties_file)
    print(b.classpath)

def _properties_from_env(args):
    Bootstrapper.write_properties_from_env(args.properties_file)

def main():
    '''
    Bootstrapper CLI
    '''
    parser = argparse.ArgumentParser(prog='kclboot', 
        description='kclboot - Kinesis Client Library Bootstrapper')

    subparsers = parser.add_subparsers(title='Subcommands', help='Additional help', dest='subparser')

    # Common arguments
    jar_path_parser = argparse.ArgumentParser(add_help=False)
    jar_path_parser.add_argument('--jar-folder', dest='jar_folder', default='./jars',
        help='Folder used to store jar files')

    prop_path_parser = argparse.ArgumentParser(add_help=False)
    prop_path_parser.add_argument('--properties-file', required=True, dest='properties_file',
        help='*.properties file with KCL settings')

    # Sub-commands
    download_parser = subparsers.add_parser('download', parents=[jar_path_parser], 
        description='Download jars necessary to run KCL\'s MultiLangDaemon')
    download_parser.set_defaults(func=_download)

    command_parser = subparsers.add_parser('command', parents=[jar_path_parser, prop_path_parser], 
        description='Output formatted Java invocation with classpath')
    command_parser.set_defaults(func=_command)

    classpath_parser = subparsers.add_parser('classpath', parents=[jar_path_parser, prop_path_parser], 
        description='Output classpath, including jars and the folder containing the *.properties file')
    classpath_parser.set_defaults(func=_classpath)

    properties_parser = subparsers.add_parser('properties-from-env', parents=[prop_path_parser], 
        description='Generate a *.properties file from environmental variables')
    properties_parser.set_defaults(func=_properties_from_env)

    args = parser.parse_args()
    if args.subparser:
        args.func(args)
    elif len(vars(args).keys()) == 1:
        parser.print_usage()
