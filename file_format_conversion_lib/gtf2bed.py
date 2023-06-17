#!/usr/bin/env python
"""
File: gtf2bed.py
Description: Convert the file format from GTF to BED
Date: 2022/4/2
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.gtf import Gtf
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(gtf_file, out_file):
    gtf_file_obj = Gtf(gtf_file)
    content = gtf_file_obj.GTF_to_BED()
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)
    else:
        print(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input GTF file.')
@click.option('-out', help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(in_file, out):
    """Convert the file format from GTF to GSDS."""
    main(in_file, out)


if __name__ == '__main__':
    run()
