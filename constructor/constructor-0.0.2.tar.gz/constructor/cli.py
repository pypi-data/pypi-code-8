from constructor import Infrastructure
import os
import imp
import argparse

def main():
    parser = argparse.ArgumentParser(description='Launch the application.')
    parser.add_argument('--env', metavar='env', type=str, help='Environment to launch in.', default='dev')
    args = parser.parse_args()

    infrastructure = Infrastructure(environment=args.env)

    blueprint = imp.load_source('blueprint', 'blueprint.py')

    blueprint.build(infrastructure)