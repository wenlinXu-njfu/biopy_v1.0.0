#!/usr/bin/env python
"""
File: gtf.py
Description: Plot gene structure based on GTF annotation file
Date: 2022/4/10
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
import matplotlib.pyplot as plt
from Biolib.gtf import Gtf


def plot_gene_structure(gtf_file: str, exon_color: str, edge_color: str, figure_width: float, figure_height: float,
                        hatch: click.Choice(['/', '|', '\\', '+', '-', 'x', '*', 'o', 'O', '.']) = None,
                        out_path: str = None, out_prefix: str = 'gene_structure', out_suffix: str = 'pdf'):
    """Plot gene structure based on GTF annotation file."""
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Arial'
    d = Gtf(gtf_file).get_gene_dict()  # {gene_id: [{start: int, end: int, strand: str}, {}, ...], ...}
    plt.figure(figsize=(figure_width, figure_height))
    exon = intron = None
    i = 0
    for gene_id, l in d.items():
        left = 0
        for exon_dict in l:
            width = exon_dict['end'] - exon_dict['start'] + 1
            exon = plt.barh(i + 1, width, left=exon_dict['start'], color=exon_color, edgecolor=edge_color, hatch=hatch)
            if left:
                right = exon_dict['start'] - 1
                intron, = plt.plot([left, right], [i + 1, i + 1], color='k', linewidth=0.4)
                left = exon_dict['end'] + 1
            else:
                left = exon_dict['end'] + 1
        i += 1
    # Set ticks and ticks label of y
    label_list = list(d.keys())
    if i >= 50:
        plt.yticks(range(1, len(label_list) + 1), label_list, size=6)
    else:
        plt.yticks(range(1, len(label_list) + 1), label_list)
    # Hide y axis and three frames
    plt.tick_params('y', color='w')
    ax = plt.gcf().gca()
    ax.spines['top'].set_color(None)
    ax.spines['right'].set_color(None)
    ax.spines['left'].set_color(None)
    # If the number of bar is too little, add some invisible lines to make bar slim
    if i <= 10:
        j = 0
        while abs(j) <= 10:
            plt.hlines(j - 1, 0, 1000, color='w')
            j -= 1
        plt.gca().spines['bottom'].set_position(('data', 0))
    # Set legend
    plt.legend([exon, intron], ['exon', 'intron'], labelcolor='g', shadow=True, loc=3, bbox_to_anchor=(0.99, 0.99))
    # Save figure
    if out_path:
        plt.savefig(f'{out_path}/{out_prefix}.{out_suffix}', bbox_inches='tight', dpi=200)
    else:
        click.echo('\033[33mWarning: No output path is specified.\033[0m', err=True)
