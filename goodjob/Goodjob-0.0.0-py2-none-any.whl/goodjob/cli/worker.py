#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

import click


@click.command()
@click.argument('args', nargs=-1)
def main(args):
    args = ['celery', 'worker', '--app=goodjob.jobs.executor'] + list(args[:])
    return subprocess.call(args)


if __name__ == '__main__':
    main()
