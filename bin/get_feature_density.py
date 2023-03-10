#!/usr/bin/env python
"""
File: get_feature_density.py
Description: Get feature density from GFF file.
Date: 2022/10/21
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.gff import Gff
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(chr_len_file, gff_file, feature, span, out_file):
    chr_len_dict = {line.split('\t')[0]: int(line.strip().split('\t')[1]) for line in open(chr_len_file)}
    content = Gff(gff_file).get_feature_density(chr_len_dict, feature, span)
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)
    else:
        print(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-len', 'chr_len_file', help='Input chromosome length file. (Chr_num\\tLength\\n)')
@click.option('-gff', help='Input GFF file.')
@click.option('-feature', help='Specify feature type. (eg. exon)')
@click.option('-span', type=int, default=100000, help='[optional] Specify density statistical span. {default=100000}')
@click.option('-out', help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(chr_len_file, gff, feature, span, out):
    """Get feature density from GFF file."""
    main(chr_len_file, gff, feature, span, out)


if __name__ == '__main__':
    run()
