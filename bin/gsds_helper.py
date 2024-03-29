#!/usr/bin/env python
"""
File: gsds_helper.py
Description: Convert the file format from GFF or GTF to GSDS
Date: 2022/3/7
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.gff import Gff
from Biolib.gtf import Gtf
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_file, file_format, feature_type, out_file):
    if file_format == 'gff':
        gff_file_obj = Gff(in_file)
        content = gff_file_obj.GFF_to_GSDS()
        if out_file:
            with open(out_file, 'w') as o:
                o.write(content)
        else:
            print(content)
    else:
        gtf_file_obj = Gtf(in_file)
        content = gtf_file_obj.GTF_to_GSDS(feature_type)
        if out_file:
            with open(out_file, 'w') as o:
                o.write(content)
        else:
            print(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input GFF or GTF file.')
@click.option('-format', 'file_format', default='gff', type=click.Choice(['gff', 'gtf']),
              help='[optional] Specify input file format. {default=gff}')
@click.option('-type', 'feature_type', type=click.Choice(['gene', 'transcript']),
              help='[optional] If input file is GTF, specify feature type. {default=transcript}')
@click.option('-out', help='[optional] Output file (id\\tstart\\tend\\tfeature\\tframe), '
                           'if not specified, print results to terminal as stdout.')
def run(in_file, file_format, feature_type, out):
    """Convert the file format from GFF or GTF to GSDS."""
    if file_format == 'gff' and feature_type:
        click.echo('\033[33mWarning: input file is GFF, type option is invalid.\033[0m', err=True)
    main(in_file, file_format, feature_type, out)


if __name__ == '__main__':
    run()
