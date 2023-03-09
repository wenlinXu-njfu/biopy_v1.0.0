#!/usr/bin/env python
"""
File: plot_gene_structure.py
Description: Plot gene structure based on annotation file
Date: 2022/3/27
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from plot_lib.gene_structure.gff import plot_mRNA_structure
from plot_lib.gene_structure.gtf import plot_gene_structure
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_file: str, in_file_format: click.Choice(['gff', 'gtf', 'bed']),
         utr_color: str, cds_color: str, exon_color: str, edge_color: str, out_path: str,
         figure_width: float, figure_height: float,
         out_format: click.Choice(['eps', 'jpeg', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz', 'tif', 'tiff']),
         utr_hatch: click.Choice(['/', '|', '\\', '+', '-', 'x', '*', 'o', 'O', '.']) = None,
         cds_hatch: click.Choice(['/', '|', '\\', '+', '-', 'x', '*', 'o', 'O', '.']) = None,
         exon_hatch: click.Choice(['/', '|', '\\', '+', '-', 'x', '*', 'o', 'O', '.']) = None):
    if in_file_format == 'gff':
        plot_mRNA_structure(in_file, utr_color, cds_color, figure_width, figure_height,
                            out_path=out_path, out_suffix=out_format, utr_hatch=utr_hatch, cds_hatch=cds_hatch)
    elif in_file_format == 'gtf':
        plot_gene_structure(in_file, exon_color, edge_color, figure_width, figure_height, exon_hatch,
                            out_path, out_suffix=out_format)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input file.')
@click.option('-type', 't', type=click.Choice(['gff', 'gtf', 'bed']), default='gff',
              help='[optional] Specify the format of input file. {default=gff}')
@click.option('-utr_color', default='salmon',
              help='[optional] If input GFF file, specify color of utr, it supports color code. {default=salmon}')
@click.option('-utr_hatch', default=None, type=click.Choice(['/', '|', '\\', '+', '-', 'x', '*', 'o', 'O', '.']),
              help='[optional] If input GFF file, specify hatch of utr. {default=None}')
@click.option('-cds_color', default='skyblue',
              help='[optional] If input GFF file, specify color of utr, it supports color code. {default=skyblue}')
@click.option('-cds_hatch', default=None, type=click.Choice(['/', '|', '\\', '+', '-', 'x', '*', 'o', 'O', '.']),
              help='[optional] If input GFF file, specify hatch of cds. {default=None}')
@click.option('-exon_color', default='salmon',
              help='[optional] If input GTF file, specify color of exon, it supports color code. {default=salmon}')
@click.option('-exon_hatch', default=None, type=click.Choice(['/', '|', '\\', '+', '-', 'x', '*', 'o', 'O', '.']),
              help='[optional] If input GTF file, specify hatch of exon. {default=None}')
@click.option('-edge_color', default=None, help='Set edge color. {default=None}')
@click.option('-figure_width', type=float, default=20.0, help='[optional] Specify output figure width. {default=20.0}')
@click.option('-figure_height', type=float, default=10.0, help='[optional] Specify output figure height. {default=10.0}')
@click.option('-out', help='Specify output file path.')
@click.option('-format', 'f', default='pdf',
              type=click.Choice(['eps', 'jpeg', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'svgz', 'tif', 'tiff']),
              help='[optional] Specify output file format. {default=pdf}')
def run(in_file, t, utr_color, utr_hatch, cds_color, cds_hatch, exon_color, exon_hatch, edge_color,
        figure_width, figure_height, out, f):
    """Plot gene structure based on annotation file."""
    if t == 'gff':
        if exon_hatch or exon_color != 'lightyellow':
            click.echo('\033[33mWarning: There are conflicting options, ignore "exon_color" and "exon_hatch".\033[0m')
    elif t == 'gtf':
        if utr_color != 'salmon' or utr_hatch or cds_color != 'skyblue' or cds_hatch:
            click.echo('\033[33mWarning: There are conflicting options, ignore "utr_color", "utr_hatch", "cds_color" and "cds_hatch".\033[0m')
    main(in_file, t, utr_color, cds_color, exon_color, edge_color, out, figure_width, figure_height, f, utr_hatch, cds_hatch, exon_hatch)


if __name__ == '__main__':
    run()
