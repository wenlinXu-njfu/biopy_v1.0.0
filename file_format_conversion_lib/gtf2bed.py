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
    content = ''
    for line in Gtf(gtf_file).GTF_to_BED():
        if out_file:
            content += line
        else:
            print(line.strip())
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-gtf', help='Input GTF file.')
@click.option('-bed', help='[optional] Output BED file, if not specified, print results to terminal as stdout.')
def run(gtf, bed):
    """Convert the file format from GTF to BED."""
    main(gtf, bed)


if __name__ == '__main__':
    run()
