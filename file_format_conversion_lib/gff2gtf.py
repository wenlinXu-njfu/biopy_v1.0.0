#!/usr/bin/env python
"""
File: gff2gtf.py
Description: Convert the file format from GFF to GTF
Date: 2022/3/23
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.gff import Gff
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(gff_file, gtf_file=None):
    gff_file_obj = Gff(gff_file)
    content = gff_file_obj.GFF_to_GTF()
    if gtf_file:
        with open(gtf_file, 'w') as o:
            o.write(content)
    else:
        print(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-gff', help='Input GFF file.')
@click.option('-gtf', help='[optional] Output GTF file, if not specified, print results to terminal as stdout.')
def run(gff, gtf):
    """Convert the file format from GFF to GTF."""
    main(gff, gtf)


if __name__ == '__main__':
    run()
