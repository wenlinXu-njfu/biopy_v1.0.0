#!/usr/bin/env python
"""
File: gff2bed.py
Description: Convert the file format from GFF to BED
Date: 2022/3/23
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.gff import Gff
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(gff_file, feature_type, bed_file):
    gff_file_obj = Gff(gff_file)
    if feature_type:
        feature_type = feature_type.split(',')
    content = gff_file_obj.GFF_to_BED(feature_type)
    if bed_file:
        with open(bed_file, 'w') as o:
            o.write(content)
    else:
        print(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-gff', help='Input GFF file.')
@click.option('-type', 'feature_type', default=None,
              help='[optional] Specify the type of feature to convert to BED format, multiple types are separated '
                   'by commas. {default=all}')
@click.option('-bed', help='[optional] Output BED file, if not specified, print results to terminal as stdout.')
def run(gff, feature_type, bed):
    """Convert the file format from GFF to BED."""
    main(gff, feature_type, bed)


if __name__ == '__main__':
    run()
