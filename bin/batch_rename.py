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


def main(in_dir, old, new, out_dir):
    files = os.listdir(in_dir)
    for file in files:
        if new:
            s = re.sub(old, new, file)
        else:
            s = re.sub(old, '', file)
        if out_dir:
            if not os.path.exists(out_dir):
                os.mkdir(out_dir)
            os.rename(f'{in_dir}/{file}', f'{out_dir}/{s}')
        else:
            os.rename(f'{in_dir}/{file}', f'{in_dir}/{s}')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-dir', 'in_dir', help='The directory where the file to be renamed resides.')
@click.option('-old', help='The string to be replaced, it supports for regular expressions')
@click.option('-new', help='[optional] Replacement string, it supports for regular expressions')
@click.option('-out', help='[optional] Output directory, if not specified, output is in the input directory')
def run(in_dir, old, new, out):
    """
    Batch rename files
    """
    main(in_dir, old, new, out)


if __name__ == '__main__':
    run()
