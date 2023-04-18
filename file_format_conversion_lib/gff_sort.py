#!/usr/bin/env python
"""
File: gff_sort.py
Description: Sort the GFF file by sequence ID
Date: 2022/3/31
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.gff import Gff
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(gff_file, out_file):
    gff_file_obj = Gff(gff_file)
    content = gff_file_obj.sort_by_id()
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)
    else:
        print(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input unsorted GFF file.')
@click.option('-out', help='[optional] Output sorted GFF file, if not specified, print results to terminal as stdout.')
def run(in_file, out):
    """Sort the GFF file by sequence ID."""
    main(in_file, out)


if __name__ == '__main__':
    run()
