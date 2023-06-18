#!/usr/bin/env python
"""
File: batch_rename.py
Description: Batch rename files
Date: 2021-10-06
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import os
import re
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_dir, old, new):
    files = os.listdir(in_dir)
    for file in files:
        if new:
            s = re.sub(old, new, file)
        else:
            s = re.sub(old, '', file)
        os.rename(f'{in_dir}/{file}', f'{in_dir}/{s}')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-dir', 'in_dir', help='The directory where the file to be renamed resides.')
@click.option('-old', help='The string to be replaced, it supports for regular expressions')
@click.option('-new', help='[optional] Replacement string, it supports for regular expressions')
def run(in_dir, old, new):
    """
    Batch rename files
    """
    main(in_dir, old, new)


if __name__ == '__main__':
    run()
