#!/usr/bin/env python
"""
File: plot_venn.py
Description: Draw the venn plot
Date: 2022/2/22
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import os
from venn import venn
import matplotlib.pyplot as plt
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_dir: str, figure_size: tuple, out_prefix: str, fmt: str):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Arial'
    files = os.listdir(in_dir)
    data_set_dict = {}
    for file in files:
        data_set_dict[file] = set(line.strip() for line in open(f'{in_dir}/{file}') if line.strip())
    venn(data_set_dict, legend_loc=(0.8, 0.8), figsize=figure_size)
    if out_prefix and fmt:
        plt.savefig(f'{out_prefix}.{fmt}')
    elif out_prefix and not fmt:
        plt.savefig(f'{out_prefix}.pdf')
    elif not out_prefix and fmt:
        plt.savefig(f'out.{fmt}', bbox_inches='tight')
    else:
        plt.savefig('out.pdf', bbox_inches='tight')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_dir', help='Input directory where data files are stored.')
@click.option('-figure_size', default='8x8', help='[optional] Specify figure size. {default=8x8}')
@click.option('-out', help='Prefix of output file. {default out.pdf}')
@click.option('-fmt', help='Specify the format of output file. {default=pdf}')
def run(in_dir, figure_size, out, fmt):
    """Draw the venn plot."""
    figure_size = tuple(float(i) for i in figure_size.split('x'))
    main(in_dir, figure_size, out, fmt)


if __name__ == '__main__':
    run()
